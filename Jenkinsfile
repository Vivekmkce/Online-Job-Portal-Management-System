pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                sh 'python3 -m venv venv && . venv/bin/activate && pip install django'
            }
        }
        stage('Check') {
            steps {
                sh '. venv/bin/activate && python manage.py check'
            }
        }
    }
}
