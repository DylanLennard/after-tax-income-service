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
              withEnv(["HOME=${env.WORKSPACE}"]){
                  sh '''pip install --user -r requirements.txt
                        python -m unittest test.py
                     '''
                  echo 'figure out how to report if the tests passed or not'
              }
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