pipeline {
  environment {
      // use these in the future instead of hardcoding like below
      registry = '38373517759.dkr.ecr.us-west-2.amazonaws.com/'
      dockerImage = 'testrepo'
      dockerTag = 'testtag'
    }
    agent any
    stages {
        stage('Build Image') {
            agent any
            steps {
              script{
                  sh '''docker build -t testrepo .
                        docker tag testrepo:latest 838373517759.dkr.ecr.us-west-2.amazonaws.com/testrepo:testtag
                     '''
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
                          python -m pytest --verbose --junit-xml test-reports/results.xml
                       '''
                    echo 'figure out how to report if the tests passed or not'
                }
                post {
                    always {
                        // Archive unit tests for the future
                        junit allowEmptyResults: true, testResults: 'test-reports/results.xml'
                    }
                }
            }
        }
        stage('Deploy') {
            agent any
            steps{
                  sh '''$(aws ecr get-login --no-include-email --region us-west-2)
                        docker push 838373517759.dkr.ecr.us-west-2.amazonaws.com/testrepo:testtag
                     '''
                  echo 'Deploy was successful'
            }
        }
    }
}
