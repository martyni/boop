pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building..'
                sh 'bash jenkins/build.sh'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
                sh 'pwd'
                sh 'bash jenkins/test.sh'
                sh 'kill $PID || exit $EXIT'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
                sh 'bash jenkins/deploy.sh'
            }
        }
    }
}
