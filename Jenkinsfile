pipeline {
    agent any

    environment {
        // Use Windows paths for the virtual environment
        VENV_DIR = ".venv"
        PYTHON = "${env.WORKSPACE}\\${env.VENV_DIR}\\Scripts\\python.exe"
        PIP = "${env.WORKSPACE}\\${env.VENV_DIR}\\Scripts\\pip.exe"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Prepare Python') {
            steps {
                // Use 'bat' instead of 'sh' for Windows
                bat """
                    python -m venv ${VENV_DIR}
                    "${PIP}" install --upgrade pip
                    if exist requirements.txt (
                        "${PIP}" install -r requirements.txt
                    )
                """
            }
        }
        
        stage('Test') {
            steps {
                bat """
                    if not exist reports mkdir reports
                    "${PYTHON}" -m pytest --junitxml=reports/junit.xml || exit 0
                """
            }
            post {
                always {
                    junit 'reports/junit.xml'
                }
            }
        }
    }
    // ... rest of your post actions
}
