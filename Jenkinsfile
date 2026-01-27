pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Code already checked out from Git'
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                python3 --version
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run ML Script') {
            steps {
                sh '''
                . venv/bin/activate
                python train.py
                '''
            }
        }
    }

    post {
        success {
            echo '✅ ML pipeline completed successfully'
        }
        failure {
            echo '❌ ML pipeline failed'
        }
    }
}
