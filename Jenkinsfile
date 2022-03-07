pipeline {
    agent { label 'ec2-fleet' }


    stages {
        stage('Build Simple WebServer') {
            when { anyOf { branch "master"; branch "dev" }}
            steps {
                echo 'Building..'
                sh '''
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
        stage('Provisioning - Dev') {
            when { allOf { branch "dev"; changeset "infra/**/*.tf" } }
            steps {
                echo 'Provisioning....'
                sh 'cd infra/dev'
                // sh 'terraform init'
                // copyArtifacts filter: 'infra/dev/terraform.tfstate', projectName: '${JOB_NAME}'
                // archiveArtifacts artifacts: 'infra/dev/terraform.tfstate', onlyIfSuccessful: true
            }
    }
}