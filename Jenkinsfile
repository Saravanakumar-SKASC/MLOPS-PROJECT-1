pipeline{
    agent any

    stages{
        stage('Cloning Github repo to jenkins'){
            steps{
                scripts{
                    echo 'Cloning Github repo to Jenkins................'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/Saravanakumar-SKASC/MLOPS-PROJECT-1.git']])
                }
            }
        }
    }
}