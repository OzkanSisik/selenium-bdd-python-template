pipeline {
    agent {
        docker { image 'python:3.11' }
    }
    environment {
        S3_BUCKET_NAME = 'ozkanbucket'
        S3_REGION = 'eu-central-1'
        AWS_CREDS = credentials('aws-s3-credentials')
    }
    stages {
        stage('Install dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Run S3 Integration Test') {
            steps {
                sh '''
                    AWS_ACCESS_KEY_ID=$AWS_CREDS_USR \
                    AWS_SECRET_ACCESS_KEY=$AWS_CREDS_PSW \
                    S3_BUCKET_NAME=$S3_BUCKET_NAME \
                    S3_REGION=$S3_REGION \
                    ENVIRONMENT=staging \
                    python3 test_s3_integration.py
                '''
            }
        }
    }
} 