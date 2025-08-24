pipeline {
    agent any

    triggers {
        githubPush()
    }

    environment {
        DOCKER_IMAGE = "manan3699/chatbot"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/BMK07/Chatbot.git',
                    credentialsId: 'Git-Pass-Bk'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:latest")
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {
                        docker.image("${DOCKER_IMAGE}:latest").push()
                    }
                }
            }
        }

        stage('Run Container') {
            steps {
                script {
                    // Stop old container if running
                    sh 'docker stop chatbot || true && docker rm chatbot || true'
                }

                // Inject .env file from Jenkins Credentials
                withCredentials([file(credentialsId: 'Env-Keys', variable: 'ENV_FILE')]) {
                    sh """
                        docker run -d -p 8501:8501 --name chatbot \
                        --env-file $ENV_FILE \
                        ${DOCKER_IMAGE}:latest
                    """
                }
            }
        }
    }
}

