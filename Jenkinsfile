pipeline {
    agent any

    environment {
        DOCKER_IMAGE = '4769/flask-restapi:flask-app'
        REGISTRY = '4769/flask-restapi'
    }

    stages {
        stage('Checkout Source') {
            steps {
                echo "App is being accessed from main brach of GitHub Repository" 
                git branch: 'main', url: 'https://github.com/jogiraju/flask_pg-rest-api.git'
            }
        }
        stage('Display Build Number') {
            steps {
                echo "The current build number is: ${env.BUILD_NUMBER}"
            }
        }
        stage('Build Docker Image') {
            steps {
                echo "Docker image is being built"
                sh 'docker build -t ${DOCKER_IMAGE}_${env.BUILD_NUMBER} .'
            }
        }
        stage('Push Docker Image and Update Helm') {
            steps {
                echo "Using the docker credentials pusing the image to Docker Hub"
                withCredentials([usernamePassword(credentialsId: 'docker-hub-cred', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh 'echo $PASS | docker login -u $USER --password-stdin'
                    sh 'docker push ${DOCKER_IMAGE}_${env.BUILD_NUMBER}'
                }
                 sh'''
                      sed -i 's|Tag: "FLASK_APP.*"|Tag: "FLASK_APP_${env.BUILD_NUMBER}"|g' flask-restapi-chart/values.yaml
                      git config user.email 'rajujogi.t@gmail.com'
                      git config user.name 'jogiraju'
                      git add flask-restapi-chart/values.yaml
                      git commit -m 'Update image tag to ${env.BUILD_NUMBER}'
                      git push origin main
                 '''
            }
        }
    }
}
