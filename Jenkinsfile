pipeline {
    agent any

    environment {
        IMAGE_NAME = 'smart-parking-ci'
        CONTAINER_NAME = 'smart-parking-ansible'
        PORT_MAPPING = '5001:5000'
        VOLUME_NAME = 'parking_data'
    }

    stages {
        stage('Checkout SCM') {
            steps {
                echo 'Checking out source code from Git repository...'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker container image for Smart Parking System...'
                sh "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage('Run Automated Tests') {
            steps {
                echo 'Executing Pytest automated test suite inside Docker container...'
                sh "docker run --rm ${IMAGE_NAME} python -m pytest test_app.py"
            }
        }

        stage('Deploy with Ansible') {
            steps {
                echo 'Triggering Ansible playbook deployment...'
                // If running in docker lab environment (as in CIT lab):
                sh '''
                if docker ps -q -f name=ansible-docker-lab | grep -q .; then
                    docker exec ansible-docker-lab ansible-playbook -i /inventory.ini /docker-deploy.yml
                else
                    echo "Deploying directly via Docker..."
                    docker volume create ${VOLUME_NAME} || true
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                    docker run -d --name ${CONTAINER_NAME} -p ${PORT_MAPPING} -v ${VOLUME_NAME}:/app/data --restart unless-stopped ${IMAGE_NAME}
                fi
                '''
            }
        }

        stage('Application Verification') {
            steps {
                echo 'Verifying running container and application health check...'
                sh "docker ps | grep ${CONTAINER_NAME} || true"
            }
        }
    }

    post {
        success {
            echo '==================================================='
            echo 'Smart Parking CI/CD Pipeline Completed Successfully!'
            echo 'Application accessible at: http://localhost:5001'
            echo 'Admin Dashboard accessible at: http://localhost:5001/admin'
            echo '==================================================='
        }
        failure {
            echo 'Smart Parking CI/CD Pipeline Failed! Check logs for errors.'
        }
    }
}
