pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building..'
                sh 'bash build.sh'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
                sh 'pwd'
                sh 'source env/bin/activate'
                sh 'poop'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
                sh 'source env/bin/activate'
                sh 'poop'
            }
        }
    }
}
