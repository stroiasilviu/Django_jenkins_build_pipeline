pipeline {
    agent any

    environment {
        VENV_DIR = 'env'  // Directory for the virtual environment
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    def projectDir = "${env.WORKSPACE}/Django_jenkins_build_pipeline"
                    
                    // Print environment variables to debug
                    sh 'env'
                    
                    // Ensure directory exists and is writable
                    sh "mkdir -p ${projectDir}"
                    sh "chmod -R 755 ${projectDir}"
                    
                    // Clean up the directory
                    sh "rm -rf ${projectDir}/*"
                    
                    // Print the current user
                    sh "whoami"
                    
                    // Print the directory contents before cloning
                    sh "ls -l ${projectDir}"
                    
                    // Clone the repository
                    sh "git clone https://github.com/stroiasilviu/Django_jenkins_build_pipeline.git ${projectDir}"
                    
                    // Print the directory contents after cloning
                    sh "ls -l ${projectDir}"
                    
                    // Change to the project directory
                    dir(projectDir) {
                        // Checkout the specific branch
                        sh 'git checkout dev'
                        
                        // Print the directory contents after checkout
                        sh "ls -l"
                    }
                }
            }
        }

        stage('Set Up Virtual Environment') {
            steps {
                script {
                    def projectDir = "${env.WORKSPACE}/Django_jenkins_build_pipeline"
                    
                    // Create virtual environment in the project directory
                    sh "python3 -m venv ${projectDir}/${env.VENV_DIR}"
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    def projectDir = "${env.WORKSPACE}/Django_jenkins_build_pipeline"
                    
                    // Activate virtual environment and install dependencies
                    sh """
                        . ${projectDir}/${env.VENV_DIR}/bin/activate
                        pip install -r ${projectDir}/requirements.txt
                    """
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    def projectDir = "${env.WORKSPACE}/Django_jenkins_build_pipeline"
                    
                    // Activate virtual environment and run tests
                    sh """
                        . ${projectDir}/${env.VENV_DIR}/bin/activate
                        cd ${projectDir}
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
                sh 'python3 setup.py sdist'
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