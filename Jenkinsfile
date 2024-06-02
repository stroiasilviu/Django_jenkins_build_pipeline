pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'  // Directory for the virtual environment
        // somecode here
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
                    sh '''
                        . ${VENV_PATH}/bin/activate
                        ${VENV_PATH}/bin/flake8 .
                    '''
                }
            }
        }

        stage('Build') {
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

