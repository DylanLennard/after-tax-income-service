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
            agent docker { image python:3.6-slim }
            steps {
                sh 'pip install -r requirements.txt'
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