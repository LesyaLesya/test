pipeline {
    agent any

    stages {
        stage('DockerBuildAndRun') {
            steps {
                sh '/usr/local/bin/docker build -t tests .'
            }
        }
        stage('Test') {
            steps {
                sh '/usr/local/bin/docker run --name my_container tests --login ${LOGIN} --passw ${PASSW} -n ${NODES}'
            }
        }
    }

    post {

        always {

            sh '/usr/local/bin/docker cp my_container:/app/allure-results .'

            script {
                allure([
                        includeProperties: false,
                        jdk: '',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: 'allure-results']]
                ])
            }

            sh '/usr/local/bin/docker system prune -f'
            sh '/usr/local/bin/docker image rm tests'


            cleanWs()
        }
    }
}
