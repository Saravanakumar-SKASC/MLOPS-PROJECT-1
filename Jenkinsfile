pipeline{
    agent any

    environment{
        VENV_DIR = 'venv'
        GCP_PROJECT = "resolute-fold-458114-c1"
        GCLOUD_PATH = "var/jenkins_home/google-cloud-sdk/bin"
    }

    stages{
        stage('Cloning Github repo to jenkins'){
            steps{
                script{
                    echo 'Cloning Github repo to Jenkins................'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/Saravanakumar-SKASC/MLOPS-PROJECT-1.git']])
                }
            }
        }
        stage('setting up our Virtual Environment and installing dependancies'){
            steps{
                script{
                    echo 'setting up our Virtual Environment and installing dependancies................'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }
        stage('Building and pushing docker image to GCR'){
            steps{
               withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Building and pushing docker image to GCR..............'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}

                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud auth configure-docker --quiet

                        docker build -t gcr.io/${GCP_PROJECT}/ml-project:latest .

                        docker push gcr.io/${GCP_PROJECT}/ml-project:latest
                        '''
                    }
               }
            }
        }
        stage('deploy to google cloud run'){
            steps{
               withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'deploy to google cloud run..............'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}

                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud run deploy ml-project \
                            --image=gcr.io/${GCP_PROJECT}/ml-project:latest \
                            --platform=managed \
                            --region=us-central1 \
                            --allowed-unauthenticated
                        
                        '''
                    }
               }
            }
        }
    }
}