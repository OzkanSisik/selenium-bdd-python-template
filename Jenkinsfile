pipeline {
    agent {
        docker { image 'ozkansisik/otoframework-ci:latest' }
    }
    environment {
        S3_BUCKET_NAME = 'ozkanbucket'
        S3_REGION = 'eu-central-1'
        ENVIRONMENT = 'staging'
    }
    stages {
        stage('Show environment.py') {
            steps {
                sh 'cat features/environment.py | head -40'
            }
        }
        stage('Check ChromeDriver') {
            steps {
                sh 'ls -l /usr/local/bin/chromedriver || echo "ChromeDriver not found!"'
                sh '/usr/local/bin/chromedriver --version || echo "ChromeDriver version check failed!"'
            }
        }
        stage('Check Google Chrome') {
            steps {
                sh 'which google-chrome || echo "Google Chrome not found!"'
                sh 'google-chrome --version || echo "Google Chrome version check failed!"'
            }
        }
        stage('List Chrome Processes') {
            steps {
                sh 'ps aux | grep chrome || echo "No chrome process found"'
            }
        }
        stage('List /var/tmp') {
            steps {
                sh 'ls -l /var/tmp || echo "/var/tmp not accessible"'
            }
        }
        stage('Run Demoblaze Authentication Test') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'aws-s3-credentials', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    sh '''
                        S3_BUCKET_NAME=$S3_BUCKET_NAME \
                        S3_REGION=$S3_REGION \
                        behave features/demoblaze_authentication.feature
                    '''
                }
            }
        }
    }
} 