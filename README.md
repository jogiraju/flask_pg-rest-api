#flask sqlalchemy postgres rest-api app
#build the image
docker build -t 4769/flask-restapi:flask-app .
#push the image to docker repository: 4769/flask_pg_rest-api with tag:flask-app
docker login -n4769
(if required)
docker push 4769/flask-restapi:flask-app
