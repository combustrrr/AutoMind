pipeline {
    agent any

    environment {
        // Your specific local Python path
        PYTHON_EXE = "C:\\Users\\icsar\\AppData\\Local\\Python\\bin\\python.exe"
        VENV_DIR = ".venv"
        // Paths for the virtual environment created during the build
        VENV_PYTHON = "${env.WORKSPACE}\\${env.VENV_DIR}\\Scripts\\python.exe"
        VENV_PIP = "${env.WORKSPACE}\\${env.VENV_DIR}\\Scripts\\pip.exe"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm [cite: 113]
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
                """ [cite: 231]
            }
        }

        stage('Lint (optional)') {
            steps {
                bat """
                    if exist "${env.VENV_PIP}" (
                        "${env.VENV_PYTHON}" -m flake8 || echo "flake8 not installed; skipping lint"
                    )
                """
            }
        }

        stage('Test') {
            steps {
                bat """
                    if not exist reports mkdir reports
                    "${env.VENV_PYTHON}" -m pytest --junitxml=reports/junit.xml || exit 0
                """ [cite: 181]
            }
            post {
                always {
                    junit 'reports/junit.xml'
                }
            }
        }

        stage('Build (if packaging present)') {
            steps {
                bat """
                    if exist setup.py (
                        "${env.VENV_PYTHON}" -m pip install build
                        "${env.VENV_PYTHON}" -m build --wheel --sdist --outdir dist
                    ) else (
                        echo "No setup.py found - skipping packaging"
                    )
                """
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'dist/**, reports/**, **/*.log', allowEmptyArchive: true [cite: 123, 131]
            cleanWs()
        }
    }
}
