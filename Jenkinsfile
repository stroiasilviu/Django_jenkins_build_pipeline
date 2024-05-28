pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Checking-out the code from the repo.
                Checkout scm
                sleep 10
            }
        }

    stage('Install Dependencies') {
        steps {
            // Installing required Python packages
            sh 'pip install -r requirements.txt'
        }
    }

    stage('Run Migrations') {
        steps{
            // Apply database migrations
            sh 'python3 manage.py migrate'
        }
    }
    
    stage('Run Tests') {
        steps {
            // Run Django tests
            sh 'python3 manage.py test'
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