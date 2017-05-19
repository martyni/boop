pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building..'
                sh 'pwd'
                sh 'virtualenv env'
                sh 'source env/bin/activate'
                sh 'pip install .' 
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
