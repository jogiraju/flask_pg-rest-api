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
                sh 'docker build -t ${DOCKER_IMAGE} .'
                echo "Docker image is being tagged"
                sh "docker image tag ${DOCKER_IMAGE} ${REGISTRY}:flask-app_${env.BUILD_NUMBER}"
            }
        }
        stage('Push Docker Image and Update Helm') {
            environment {
               NEW_DOCKER_IMAGE = "${DOCKER_IMAGE}_${env.BUILD_NUMBER}"
            }
            steps {
                echo "Using the docker credentials pusing the image to Docker Hub"
                withCredentials([usernamePassword(credentialsId: 'docker-hub-cred', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh 'echo $PASS | docker login -u $USER --password-stdin'
                    sh 'docker push ${NEW_DOCKER_IMAGE}'
                }
                git branch: 'main', url: 'https://github.com/jogiraju/argo-flask-restapi.git'
                withCredentials([usernamePassword(credentialsId: 'my-github', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD')]) {
                   sh '''
                      sed -i 's|tag: "flask-app.*"|tag: "flask-app_${env.BUILD_NUMBER}"|g' values.yaml
                      git config --global user.name "${GIT_USERNAME}"
                      git config --global user.password "${GIT_PASSWORD}"
                      git add values.yaml
                      git commit -m 'Update image tag to ${env.BUILD_NUMBER}'
                      git push --set-upstream origin main
                   '''
                }
            }
        }
    }
}
