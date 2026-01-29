pipeline {
    agent any

    environment {
        // Updated with your local path
        PYTHON_EXE = "C:\\Users\\icsar\\AppData\\Local\\Python\\bin\\python.exe"
        VENV_DIR = ".venv"
        VENV_PYTHON = "${env.WORKSPACE}\\${env.VENV_DIR}\\Scripts\\python.exe"
        VENV_PIP = "${env.WORKSPACE}\\${env.VENV_DIR}\\Scripts\\pip.exe"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Prepare Python') {
            steps {
                bat """
                    "${env.PYTHON_EXE}" -m venv ${VENV_DIR}
                    "${env.VENV_PIP}" install --upgrade pip
                    if exist requirements.txt (
                        "${env.VENV_PIP}" install -r requirements.txt
                    )
                """
            }
        }

        stage('Test') {
            steps {
                bat """
                    if not exist reports mkdir reports
                    "${env.VENV_PYTHON}" -m pytest --junitxml=reports/junit.xml || exit 0
                """
            }
            post {
                always {
                    junit 'reports/junit.xml'
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/**, **/*.log', allowEmptyArchive: true
            cleanWs()
        }
    }
}
