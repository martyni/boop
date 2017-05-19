pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'python setup.py install' 
                echo 'Building..'
            }
        }
        stage('Test') {
            steps {
                sh 'poop'
                echo 'Testing..'
            }
        }
        stage('Deploy') {
            steps {
                sh 'poop'
                echo 'Deploying....'
            }
        }
    }
}
