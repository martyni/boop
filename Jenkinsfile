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
                sh 'bash jenkins/setup.sh'
                sh 'bash jenkins/test.sh localhost:5000'
                sh 'bash jenkins/tear_down.sh'
                sh 'kill $(cat /tmp/PID) || exit $(cat /tmp/EXIT)'
                sh 'rm /tmp/PID && rm /tmp/EXIT'
            }
        }
        stage('Deploy Dev') {
            steps {
                echo 'Deploying....'
                sh 'bash jenkins/deploy_dev.sh'
                sh 'cat url'
            }
        }
        stage('Test Dev') {
            steps {
                echo 'Testing..'
                sh 'pwd'
                sh 'bash jenkins/test.sh $(cat url)'
                sh 'kill $(cat /tmp/PID) || exit $(cat /tmp/EXIT)'
                sh 'rm /tmp/PID && rm /tmp/EXIT'
            }
        }
    }
}
