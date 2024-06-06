pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'  // Directory for the virtual environment
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
                script {
                    // Start the Django development server in the background
                    sh 'nohup ./venv/bin/python manage.py runserver 0.0.0.0:8000 &'

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
                    sh './static_scan.sh'
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

    
        stage('Build Docker Image') {
            steps {
                script {
                    // Ensure the Dockerfile is in the correct location and build the Docker image
                    sh '''
                        if [ ! -f Dockerfile ]; then
                            echo "Dockerfile not found!"
                            exit 1
                        fi
                        docker build -t ssilviu11/django_project:latest .
                        docker images
                    '''
                }
            }
        }

        stage('Publish Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: '47ef7b53-2a31-476f-9df5-85e1c72cf275', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    script {
                        sh '''
                            docker login -u $DOCKER_USER -p $DOCKER_PASS
                            docker tag ssilviu11/django_project:latest ssilviu11/django_project:latest
                            docker push ssilviu11/django_project:latest
                        '''
                    }
                }
            }
        }

        stage('Deploy Container and Test') {
            steps {
                script {
                    // Ensure the container is started with the correct ports and check logs
                    sh 'docker run -d -p 4000:8000 --name app ssilviu11/django_project:latest'
                    sleep 10
                    sh 'docker ps -a' // List all containers for debugging purposes
                    sh 'docker logs app' // Check logs of the running container for debugging
                    sh 'curl -f http://localhost:4000 || exit 1'
                }
            }
        }

        stage('Clean-up containers and images') {
            steps {
                script {
                    // Clean up any existing containers
                    sh '''
                        if docker container ls -a | grep app ;
                        then
                            docker container stop app
                            docker container rm app
                        fi
                    '''
                    
                    // Clean up dangling images
                    // sh 'docker image prune -f'
                        
                    // Remove specific image
                    sh '''
                        if docker image ls -a | grep ssilviu11/django_project ;
                        then
                            docker image rm ssilviu11/django_project:latest
                        fi
                    '''
                }
            }
        }
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
