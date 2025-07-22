pipeline {
    agent any
    environment {
        S3_BUCKET_NAME = 'ozkanbucket'
        S3_REGION = 'eu-central-1'
        // aws-s3-credentials, "Username with password" olarak tanımlı olmalı
        AWS_ACCESS_KEY_ID = credentials('aws-s3-credentials', 'username')
        AWS_SECRET_ACCESS_KEY = credentials('aws-s3-credentials', 'password')
    }
    stages {
        stage('Install dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Run S3 Integration Test') {
            steps {
                sh 'ENVIRONMENT=staging python3 test_s3_integration.py'
            }
        }
    }
} 