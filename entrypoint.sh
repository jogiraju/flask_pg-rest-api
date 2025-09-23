#!/bin/bash
# entrypoint.sh

set -e

echo "Running entrypoint.sh"
echo "$DATABASE_URL"

DB_HOST=$(echo $DATABASE_URL | sed -E 's/.*@([^:/]+).*/\1/')
DB_PORT=$(echo $DATABASE_URL | sed -E 's/.*:([0-9]+)\/.*/\1/')

echo "Waiting for database at $DB_HOST:$DB_PORT ..."

#Wait until Postgres is ready
until pg_isready -h "$DB_HOST" -p "$DB_PORT" > /dev/null 2>&1; do 
    echo "Database is not ready yet, retrying..."
    sleep 2
done

echo "Database is ready!"
if [ ! -d "/app/migrations" ]; then
    echo "No migrations directory found. Initializing..."
    flask db init 
fi

if [ -z "$(ls -A /app/migrations/versions 2>/dev/null)" ]; then
    echo "No migration scripts found. Creating inital migration..."
    flask db migrate    
fi

echo "Applying migrations..."
flask db upgrade

echo "Starting Flask..."
gunicorn --bind 0.0.0.0:9000 -w 2 manage:app
