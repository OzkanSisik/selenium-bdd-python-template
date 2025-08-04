pipeline {
    agent {
        docker { image 'ozkansisik/otoframework-ci:latest' }
    }
    environment {
        S3_BUCKET_NAME = 'ozkanbucket'
        S3_REGION = 'eu-central-1'
        ENVIRONMENT = 'staging'
        HOME = '/var/jenkins_home'
    }
    stages {
        stage('Prepare .local dir') {
            steps {
                sh 'mkdir -p /var/jenkins_home/.local/share/applications && chown -R 1000:1000 /var/jenkins_home/.local && chmod -R 700 /var/jenkins_home/.local'
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