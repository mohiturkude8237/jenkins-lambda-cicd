pipeline {

    agent any

    environment {
        AWS_DEFAULT_REGION = 'ap-south-1'
        AWS_REGION = 'ap-south-1'
        VENV = 'venv'
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/mohiturkude8237/jenkins-lambda-cicd.git'
            }
        }

        stage('Verify Project') {
            steps {
                sh '''
                    echo "Current workspace:"
                    pwd

                    echo "Project files:"
                    ls -la

                    echo "Searching for SAM template:"
                    find . -maxdepth 2 -name "template.yaml" -o -name "template.yml"

                    test -f template.yaml || test -f template.yml
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv ${VENV}
                    ${VENV}/bin/python -m pip install --upgrade pip
                    ${VENV}/bin/python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Unit Testing') {
            steps {
                sh '''
                    ${VENV}/bin/python -m pytest tests/
                '''
            }
        }

        stage('Validate SAM') {
            steps {
                sh '''
                    sam validate
                '''
            }
        }

        stage('Build') {
            steps {
                sh '''
                    sam build
                '''
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
                          --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
                          --region ap-south-1 \
                          --no-confirm-changeset \
                          --no-fail-on-empty-changeset
                    '''
                }
            }
        }
    }
}
