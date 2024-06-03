pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'  // Directory for the virtual environment
        // AWS_REGION = 'eu-west-1' // e.g., us-west-2
        // AWS_ACCOUNT_ID = '471112656092' // Replace with your AWS account ID
        // IMAGE_TAG = '1.0.0'
        // ECR_REPOSITORY = 'your-ecr-repository-name' // Replace with your ECR repository name
        // DOCKER_IMAGE = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY}:${IMAGE_TAG}"
        // EC2_INSTANCE_IP = 'your-ec2-instance-ip' // Replace with your EC2 instance IP
        // SSH_KEY_PATH = '/path/to/your/private/key' // Replace with the path to your SSH private key
    }

    stages {
        stage('Install Dependencies') {
            steps {
                script {
                    // Activate the virtual environment.
                    if (isUnix()) {
                        sh './venv/bin/activate'
                    } else {
                        bat 'venv\\Scripts\\activate'
                    }
                    // Install dependencies using pip from the virtual environment
                    sh 'pip install -r requirements.txt'
                }
            }
        }

        stage('Run Migrations') {
            steps {
                script {
                    // Apply database migrations using the python executable from the virtual environment
                    sh './venv/bin/python3 manage.py migrate'
                }
            }
        }

        stage('Run Tests') {
            steps {
                // script {
                //     // Run Django tests using the python executable from the virtual environment
                //     // sh '.venv/bin/python manage.py test'
                // }
                script {
                    // Start the Django development server in the background
                    sh 'nohup ./venv/bin/python manage.py runserver 0.0.0.0:8000 &'
                    // sh './env/bin/python manage.py runserver 0.0.0.0:8000'
                    //sh 'nohup python manage.py runserver 0.0.0.0:8000 &'

                    // Wait for the server to start
                    sh 'sleep 10'

                    // Run a smoke test to check if the server is running
                    sh 'curl -f http://localhost:8000 || exit 1'

                    // Kill the Django development server
                    sh 'pkill -f runserver'
                }
            }
        }

        stage('Static Analysis') {
            steps {
                script {
                    // Run flake8 for linting using the flake8 executable from the virtual environment
                    //sh './venv/bin/flake8'
                    sh flake8
                    //  '''
                    //     . venv/bin/activate
                    //     flake8 .
                    // '''
                }
            }
        }

        stage('Build and Archive') {
            steps {
                script {
                    // Package the application
                    sh '''
                        # Create a directory for the package
                        mkdir -p build

                        # Copy necessary files to the build directory
                        cp -r ssm_app/ ssm_project/ manage.py requirements.txt build/

                        # Create an archive of the build directory
                        tar -czf build.tar.gz -C build .
                    '''
                }
                // Archive the build artifacts
                archiveArtifacts artifacts: 'build.tar.gz', followSymlinks: false
            }
        }
    
        stage('Clean-up containers') {
            steps {
                script {
                    sh '''
                        if docker container ls -a | grep app ;
                        then
                            docker container stop app
                            docker container rm app
                        fi
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t django_project:latest .'
                }
            }
        }

        stage('Publish Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: '47ef7b53-2a31-476f-9df5-85e1c72cf275', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    script {
                        sh 'docker login -u $DOCKER_USER -p $DOCKER_PASS'
                        // sh 'docker tag django_project:latest ssilviu11/django_project:latest'
                        sh 'docker push ssilviu11/django_project:latest'
                    }
                }
            }
        }

        stage('Deploy Container') {
            steps {
                script {
                    sh 'docker run -d -p 4000:8000 --name app ssilviu11/django_project:latest'
                    sleep 10
                    sh 'docker ps -a' // List all containers for debugging purposes
                    sh 'docker logs app' // Check logs of the running container for debugging
                    sh 'curl -f http://localhost:4000 || exit 1'
                }
            }
        }
        
        // stage('Publish Docker Image to EC2') {
        //     steps {
        //         script {
        //             sh '''
        //                 # Save Docker image to a tar file
        //                 docker save -o django_image.tar django_image:${IMAGE_TAG}
                        
        //                 # Transfer the tar file to the EC2 instance
        //                 scp -i ${SSH_KEY_PATH} django_image.tar ec2-user@${EC2_INSTANCE_IP}:/home/ec2-user/

        //                 # SSH into the EC2 instance and load the Docker image
        //                 ssh -i ${SSH_KEY_PATH} ec2-user@${EC2_INSTANCE_IP} << EOF
        //                 docker load -i /home/ec2-user/django_image.tar
        //                 EOF
        //             '''
        //         }
        //     }
        // }

        // stage('Deploy to AWS EC2') {
        //     steps {
        //         script {
        //             sh '''
        //                 ssh -i ${SSH_KEY_PATH} ec2-user@${EC2_INSTANCE_IP} << EOF
        //                 docker stop app || true
        //                 docker rm app || true
        //                 docker run -d -p 4000:80 --name app appimg:${IMAGE_TAG}
        //                 EOF
        //             '''
        //             sleep 10
        //             sh 'curl -k http://${EC2_INSTANCE_IP}:4000'
        //         }
        //     }
        // }
    }

    post {
        always {
            // Clean up after build
            cleanWs()
        }
        success {
            echo 'Build completed successfully!'
        }
        failure {
            echo 'Build failed!'
        }
    }
}

