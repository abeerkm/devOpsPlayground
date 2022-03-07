pipeline {
     agent { label 'ec2-fleet' }

    stages {
        stage('Build Simple WebServer-test') {
            when { anyOf { branch "master"; branch "dev" }}
            steps {
                echo 'Building..'
                sh '''
                ec2-metadata
                cd simple_webserver
                # docker build
                '''
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}
