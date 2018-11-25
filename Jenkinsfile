pipeline {
    agent any 

    stages {
        stage('Build Assets') {
            agent any 
            steps {
                echo 'Checking that this worked...'
            }
        }
        stage('Test') {
            agent any
            steps {
                echo 'Testing stuff...'
            }
        }
        stage('Deploy') {
          agent any
          steps{
                echo 'Deploying stuff...'
          }
        }
    }
}