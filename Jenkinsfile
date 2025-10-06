pipeline {
    agent any

    triggers {
        // Poll GitHub every 5 minutes
        pollSCM('H/5 * * * *')
    }

    environment {
        DOCKERHUB_CREDENTIALS = credentials('docker-cred')
        IMAGE_NAME = '4769/flask-restapi'
    }

    stages {
        stage('Check Changed Files') {
            steps {
                script {
                    // Get changed files in the latest commit
                    def changedFiles = sh(script: "git diff --name-only HEAD~1", returnStdout: true).trim().split('\n')
                    echo "Changed files:\n${changedFiles.join('\n')}"

                    // Check if any Python files in app/ changed
                    def appChanged = changedFiles.any { it ==~ /^app\\/.*\\.py$/ }
                    if (!appChanged) {
                        echo "No Python files under app/ changed — skipping pipeline."
                        currentBuild.result = 'SUCCESS'
                        //error("No relevant changes detected.")
                        return
                    }
                }
            }
        }

        stage('Determine Next Image Tag') {
            steps {
                script {
                    // Read current tag from helm-chart/values.yaml
                    def currentTag = sh(script: "grep '  tag:' helm-chart/values.yaml | awk '{print \$2}'", returnStdout: true).trim()
                    echo "Current tag in values.yaml: ${currentTag}"

                    // Toggle between 1 and 2
                    def nextTag = (currentTag == "flask-app_1") ? "flask-app_2" : "flask-app_1"
                    echo "Next tag to use: ${nextTag}"

                    // Export for later stages
                    env.IMAGE_TAG = nextTag
                }
            }
        }

        stage('Build & Push Docker Image') {
            when {
                changeset pattern: "app/**/*.py", comparator: "GLOB"
            }
            steps {
                script {
                    sh """
                        echo "Building Docker image with tag ${IMAGE_TAG}"
                        docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                        echo "${DOCKERHUB_CREDENTIALS_PSW}" | docker login -u "${DOCKERHUB_CREDENTIALS_USR}" --password-stdin
                        docker push ${IMAGE_NAME}:${IMAGE_TAG}
                    """
                }
            }
        }

        stage('Update Helm values.yaml') {
            when {
                changeset pattern: "app/**/*.py", comparator: "GLOB"
            }
            steps {
                script {
                    sh """
                        echo "Updating image tag in helm-chart/values.yaml to ${IMAGE_TAG}"
                        sed -i 's|tag: "flask-app.*|  tag: "${IMAGE_TAG}"|' helm-chart/values.yaml

                        git config user.name "jenkins-bot"
                        git config user.email "jenkins@local"
                        git add helm-chart/values.yaml
                        git commit -m "Update Helm values.yaml with image tag ${IMAGE_TAG}"
                        git push origin HEAD:main
                    """
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline completed with status: ${currentBuild.currentResult}"
        }
    }
}
