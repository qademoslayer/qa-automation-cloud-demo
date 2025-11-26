pipeline {
  agent any
  stages {
    stage('Checkout'){ steps{ checkout scm } }
    stage('Setup'){
      steps{
        sh 'python3 -m pip install --upgrade pip'
        sh 'pip3 install -r requirements.txt'
        sh 'python3 -m playwright install --with-deps'
      }
    }
    stage('Validate'){ steps{ sh 'python3 tests/validation/nea_validate.py' } }
    stage('API Tests'){
      steps{ sh 'pytest tests/api --alluredir=allure-results --html=reports/api_report.html --self-contained-html' }
    }
    stage('UI Tests'){
      environment { BASE_URL = 'https://example.com' }
      steps{ sh 'pytest tests/ui --alluredir=allure-results --html=reports/ui_report.html --self-contained-html' }
    }
    stage('Allure Report (archive)'){
      steps{ sh 'ls -la allure-results || true' }
    }
  }
  post {
    always {
      archiveArtifacts artifacts: 'reports/**, allure-results/**', fingerprint: true
      junit allowEmptyResults: true, testResults: '**/junit.xml'
    }
  }
}