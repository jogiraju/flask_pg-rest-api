pipeline {
    agent any

    environment {
        DOCKER_IMAGE = '4769/flask-restapi:flask-app'
    }

    stages {
        stage('Checkout Source') {
            steps {
                echo "App is being accessed from main branch of GitHub Repository"
                git branch: 'main', url: 'https://github.com/jogiraju/flask_pg-rest-api.git'
            }
        }
        stage('Set Variables') {
            steps {
                echo "The current build number is: ${env.BUILD_NUMBER}"
                script {
                    def ID = env.BUILD_NUMBER.toInteger() % 2 + 1
                    env.MYTAG = "${ID}"
                    env.NEW_DOCKER_IMAGE = "${DOCKER_IMAGE}_${ID}"
                }
            }
        }
        stage('Build Docker Image') {
            options {
                    timeout(time: 45, unit: 'MINUTES') 
            }
            steps {
                echo "Docker image is being built & tagged"
                echo "Building docker image with tag: ${env.MYTAG}"
                sh 'whereis docker' 
                sh'''
                  CWD=`pwd`
                  ls -l
                  cd $CWD
                  echo "$CWS"
                  docker build -t "${DOCKER_IMAGE}" -f ./Dockerfile . 
                '''
                echo "Tagged docker image: ${env.NEW_DOCKER_IMAGE}"                    
                sh "docker image tag ${DOCKER_IMAGE} ${env.NEW_DOCKER_IMAGE}"
            }
        }
        stage('Push Docker Image and Update Helm') {           
            environment {
                  NEW_TAG = "${env.NEW_DOCKER_IMAGE}"
            }
            steps {
                      echo "Using the docker credentials pusing the image to Docker Hub"
                      withCredentials([usernamePassword(credentialsId: 'docker-cred', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                          sh"""
                            echo $PASS | docker login -u $USER --password-stdin
                            docker push ${NEW_TAG} 
                          """
                      }
                      git branch: 'main', url: 'url: 'https://github.com/jogiraju/flask_pg-rest-api.git'
                      withCredentials([usernamePassword(credentialsId: 'github-cred', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD')]) {
                        sh"""
                           sed -i 's|"flask-app.*"|"flask-app_${env.MYTAG}"|g' helm-chart/values.yaml
                        """
                        sh '''
                            git add helm-chart/values.yaml
                            git commit -m 'Updated image tag'
                            git remote set-url origin https://${GIT_PASSWORD}@github.com/jogiraju/flask_pg-rest-api.git
                            git push origin main
                        '''
                      }
            }
        }
    }
}
