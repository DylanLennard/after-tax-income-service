pipeline {
    agent any 
    stages {
        stage('Build Image') {
            agent any 
            steps {
                sh 'git clone https://github.com/DylanLennard/after-tax-income-service.git'
                sh 'cd after-tax-income-service/'
                sh 'docker build -t testrepo .'
                sh 'docker tag testrepo testrepo:testtag'
            }
        }
        stage('Unit Tests') {
            agent docker {image python3.6-slim}
            steps {
                sh 'pip3 install -r requirements.txt'
                sh 'python -m unittest test.py'
                # figure out how to signify that these tests passed or nah
            }
        }
        stage('Deploy') {
            agent any
            steps{
                  echo 'Push Build to ECR...'
            }
        }
    }
}