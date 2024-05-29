pipeline {
    agent any

    environment {
        VENV_DIR = 'env'  // Directory for the virtual environment
    }

    // stages {
    //     stage('Checkout') {
    //         steps {
    //             script {
    //                 // Print environment variables to debug
    //                 sh 'env'
                    
    //                 // Manually remove any existing directory to ensure a clean state
    //                 sh 'rm -rf /home/silviu/Django_jenkins_build_pipeline || true'
                    
    //                 // Clone the repository
    //                 sh 'git clone https://github.com/stroiasilviu/Django_jenkins_build_pipeline.git'
                    
    //                 // Change to the project directory
    //                 dir('/home/silviu/Django_jenkins_build_pipeline') {
    //                     // Checkout the specific branch
    //                     sh 'git checkout dev'
                        
    //                     // Optionally, fetch all branches
    //                     // sh 'git fetch --all'
                        
    //                     // Optionally, pull the latest changes
    //                     // sh 'git pull origin main'
    //                 }
    //             }
    //         }
    //     }

        stage('Set Up Virtual Environment') {
            steps {
                script {
                    // Create virtual environment
                    sh "python -m venv ${env.VENV_DIR}"
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    // Activate virtual environment and install dependencies
                    sh """
                        . ${env.VENV_DIR}/bin/activate
                        pip install -r your-project/requirements.txt
                    """
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Activate virtual environment and run tests
                    sh """
                        . ${env.VENV_DIR}/bin/activate
                        cd /home/silviu/Django_jenkins_build_pipeline
                        python manage.py test
                    """
                }
            }
        }

    stage('Static Code Analysis') {
        steps {
            // Run flake8 for linting
            sh 'flake8 .'
        }
    }

stage('Package') {
            steps {
                // Package your application (optional)
                sh 'python setup.py sdist'
            }
        }

        stage('Deploy') {
            when {
                branch 'dev' // Deploy only if we are on the dev branch
            }
            steps {
                // Example deploy step
                sh 'echo "Deploying application..."'
                // Add your deployment steps here
            }
        }
    }

    post {
        always {
            // Archive the test results and coverage reports
            junit '**/test-results/*.xml'
            archiveArtifacts '**/dist/*.tar.gz'
        }
    }
}