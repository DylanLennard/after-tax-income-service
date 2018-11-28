pipeline {
  environment {
      registry = 'testrepo'
      dockerImage = ''
    }
    agent any 
    stages {
        stage('Cloning Git') {
            agent any 
            steps {
                git 'https://github.com/DylanLennard/after-tax-income-service.git'
            }
        }
        stage('Build Image') {
            agent any 
            steps {
              script{
                  dockerImage = docker.build registry + ':testtag'
              }
            }
        }
        stage('Unit Tests') {
            agent {
                docker { image 'python:3.6-slim' }
            }
            steps {
                sh 'python -m virtualenv testenv'
                sh 'source activate testenv'
                sh 'sudo pip install -r requirements.txt'
                sh 'sudo python -m unittest test.py'
                sh 'deactivate'
                echo 'figure out how to report if the tests passed or not'
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