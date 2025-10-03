pipeline {
    agent any

    environment {
        DOCKER_IMAGE = '4769/flask-restapi:flask-app'
        REGISTRY = '4769/flask-restapi'
    }

    stages {
        stage('Checkout Source') {
            steps {
                echo "App is being accessed from main branch of GitHub Repository"
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
                echo "Docker image is being built & tagged"
                script {
                    def ID = env.BUILD_NUMBER.toInteger() % 2 + 1
                    echo "Building docker image"
                    sh 'docker build -t ${DOCKER_IMAGE} .'
                    echo "Tagged docker image: ${DOCKER_IMAGE}_${ID}"                    
                    sh "docker image tag ${DOCKER_IMAGE} ${REGISTRY}:flask-app_${ID}"
                }                
            }
        }
        stage('Push Docker Image and Update Helm') {           
            steps {
                      echo "Using the docker credentials pusing the image to Docker Hub"
                      withCredentials([usernamePassword(credentialsId: 'docker-hub-cred', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                          sh 'echo $PASS | docker login -u $USER --password-stdin'
                          script {
                            def ID = env.BUILD_NUMBER.toInteger() % 2 + 1
                            def NEW_DOCKER_IMAGE = "${DOCKER_IMAGE}_${ID}"
                            sh 'docker push ${NEW_DOCKER_IMAGE}'
                          }                          
                      }
                      git branch: 'main', url: 'https://github.com/jogiraju/argo-flask-restapi.git'
                      script {
                        def ID = env.BUILD_NUMBER.toInteger() % 2 + 1
                        sh'''
                          sed -iE "s|"flask-app.*"|"flask-app_${ID}"|g" values.yaml
                        ''' 
                      }                      
                      withCredentials([usernamePassword(credentialsId: 'github-cred', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD')]) {
                        sh '''
                            git add values.yaml
                            git commit -m 'Updated image tag'
                            git remote set-url origin https://${GIT_PASSWORD}@github.com/jogiraju/argo-flask-restapi.git
                            git push origin main
                        '''
                      }
            }
        }
    }
}
