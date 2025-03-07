pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git credentialsId: 'github-ssh-private-key',
                    url: 'https://github.com/DestroyedTeam/ApplicationDistributionCenter.git',
                    branch: 'feat/va/clean-better'
            }
        }

        stage('Build & Test') {
            steps {
                sh '''
                    poetry lock
                    pytest testunit/tests.py  || exit 1
                '''
            }
        }

        stage('Deploy') {
            when {
                expression { currentBuild.currentResult  == 'SUCCESS' }
            }
            steps {
                sh '''
                    docker build -t application-center:latest -f Dockerfile .
                    docker push 8.130.112.207:22224/application-center:latest
                '''
            }
        }
    }

    post {
        always {
            mail to: 'zhaotongxu@helixlife.cn',
                 subject: "Jenkins Build ${currentBuild.result}:  ${env.JOB_NAME}",
                 body: "Build ${currentBuild.number}  of ${env.JOB_NAME} has completed with result ${currentBuild.result}."
        }
    }
}