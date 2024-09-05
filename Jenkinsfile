pipeline {
    agent any
    environment {
        GCP_PROJECT = 'google-cloud-project-id'
        IMAGE_NAME = "gcr.io/${GCP_PROJECT}/loan-approval-app"
    }
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/zaphod9801/MLE-challenge-loan-application.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${IMAGE_NAME}:$BUILD_NUMBER")
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://gcr.io', 'gcr:google-auth') {
                        docker.image("${IMAGE_NAME}:$BUILD_NUMBER").push()
                    }
                }
            }
        }
        stage('Deploy to Cloud Run') {
            steps {
                sh '''
                gcloud run deploy loan-approval-app \
                    --image ${IMAGE_NAME}:$BUILD_NUMBER \
                    --platform managed \
                    --region us-central1 \
                    --allow-unauthenticated \
                    --port 8000
                '''
            }
        }
    }
}
