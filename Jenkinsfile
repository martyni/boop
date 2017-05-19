pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building..'
                python setup.py install 
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
                poop 
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
                poop
            }
        }
    }
}
