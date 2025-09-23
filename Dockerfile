FROM python:3.11-slim

WORKDIR /app

#Install postgres client for pg_isready used in /entrypoint.sh 
# remove app cache
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/* 

#pip installation should be done before COPY and do not create cache directory for the pip installation
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


#This probably coping all the files recursively unider /app directory. 
COPY . .

# Copy at the route not at /app
#COPY entrypoint.sh /entrypoint.sh
RUN chmod +x entrypoint.sh

ENV FLASK_APP=manage.py
ENV FLASK_ENV=production

EXPOSE 5000

ENTRYPOINT ["/app/entrypoint.sh"]
