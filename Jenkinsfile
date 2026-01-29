pipeline {
  agent any

  environment {
    VENV_DIR = ".venv"
    PYTHON = "${env.WORKSPACE}/${env.VENV_DIR}/bin/python"
    PIP = "${env.WORKSPACE}/${env.VENV_DIR}/bin/pip"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Prepare Python') {
      steps {
        sh '''
          set -e
          python3 -V || { echo "python3 not found on agent"; exit 1; }
          rm -rf ${VENV_DIR}
          python3 -m venv ${VENV_DIR}
          ${PIP} install --upgrade pip
          if [ -f requirements.txt ]; then
            ${PIP} install -r requirements.txt
          fi
        '''
      }
    }

    stage('Lint (optional)') {
      steps {
        sh '''
          set -e
          if ${PIP} show flake8 > /dev/null 2>&1; then
            ${PYTHON} -m flake8 || true
          else
            echo "flake8 not installed; skipping lint"
          fi
        '''
      }
    }

    stage('Test') {
      steps {
        sh '''
          set -e
          mkdir -p reports
          if ${PIP} show pytest > /dev/null 2>&1; then
            ${PYTHON} -m pytest --junitxml=reports/junit.xml || true
          else
            echo "pytest not installed; skipping tests"
          fi
        '''
      }
      post {
        always {
          junit 'reports/junit.xml'
        }
      }
    }

    stage('Build (if packaging present)') {
      steps {
        sh '''
          set -e
          if [ -f setup.py ] || [ -f pyproject.toml ]; then
            ${PYTHON} -m pip install build
            ${PYTHON} -m build --wheel --sdist --outdir dist || true
          else
            echo "No setup.py or pyproject.toml found - skipping packaging"
          fi
        '''
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: 'dist/**, reports/**, **/*.log', allowEmptyArchive: true
      cleanWs()
    }
    success {
      echo "Build succeeded"
    }
    failure {
      echo "Build failed — check console output"
    }
  }
}
