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
                sh 'kill $(cat /tmp/PID) || exit $(cat /tmp/EXIT)'
                sh 'rm /tmp/PID) && rm /tmp/EXIT'
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
