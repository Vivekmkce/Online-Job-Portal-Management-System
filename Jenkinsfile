pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                bat 'python -m venv venv'
                bat 'venv\\Scripts\\python.exe -m pip install django mysqlclient'
            }
        }
        stage('Check') {
            steps {
                bat 'venv\\Scripts\\python.exe -m compileall -q jobportal members manage.py'
            }
        }
    }
}
