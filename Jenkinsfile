pipeline {
    agent any

    environment {
        DOCKER_IMAGE = '4769/flask-restapi:flask-app'
        REGISTRY = '4769/flask-restapi'
    }

    stages {
        stage('Checkout Source') {
            steps {
                git branch: 'main', url: 'https://github.com/your-org/your-flask-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${DOCKER_IMAGE} .'
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-cred', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh 'echo $PASS | docker login -u $USER --password-stdin'
                    sh 'docker push ${DOCKER_IMAGE}'
                }
            }
        }
    }
}

