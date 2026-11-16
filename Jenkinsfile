pipeline {

    agent any

    environment {
        AWS_DEFAULT_REGION = 'ap-south-1'
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/mohiturkude8237/jenkins-lambda-cicd.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m pip install -r requirements.txt
                '''
            }
        }

        stage('Unit Testing') {
            steps {
                sh 'python3 -m pytest tests/'
            }
        }

        stage('Build') {
            steps {
                sh 'sam build'
            }
        }

        stage('Approval') {
            steps {
                input message: 'Approve Lambda deployment?'
            }
        }

        stage('Deploy') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'aws-creds',
                        usernameVariable: 'AWS_ACCESS_KEY_ID',
                        passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                    )
                ]) {
                    sh '''
                        sam deploy \
                          --stack-name jenkins-lambda-cicd \
                          --resolve-s3 \
                          --capabilities CAPABILITY_IAM \
                          --region ap-south-1 \
                          --no-confirm-changeset \
                          --no-fail-on-empty-changeset
                    '''
                }
            }
        }
    }
}
