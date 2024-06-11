# Django Pipeline Project
This project is a Django web application that utilizes a Jenkins pipeline for Continuous Integration and Continuous Deployment (CI/CD). The project automates the build, test, and deployment processes using Docker and Jenkins.

## Tools and Technologies used
- Django: Python web framework used for developing the web application.
- Jenkins: Automation server used for setting up the CI/CD pipeline.
- Docker: Platform used to containerize the application.
- Docker Hub: Repository for storing Docker images.
- Python: Programming language used for the Django application.

## Project Setup
## Step 1: Clone the Repository
1. Clone the repository to your local machine:
  git clone https://github.com/stroiasilviu/Django_jenkins_build_pipeline.git
  cd Music-for-your-soul--Django-project 

2. Navigate to the project directory and create a Python virtual environment:
  python3 -m venv venv
  source venv/bin/activate

3. Install the required dependencies:
  pip install -r requirements.txt

## Step 2: Set Up Jenkins
1. Install Jenkins on your server or local machine.
2. Install the necessary Jenkins plugins (e.g., Docker, Git, Python).
3. Create a new Jenkins job and link it to your GitHub repository.


## Step 3: Set Up Docker
1. Create a Dockerfile in your project root to define the Docker image:

Dockerfile:
```
ROM python:3.10.12
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

2. Build and run the Docker container to test locally:
bash:

```
docker build -t ssilviu11/django_project:latest .
docker run -d -p 4000:8000 --name app ssilviu11/django_project:latest
```

## Pipeline Stages:
## Stage 1: Install Dependencies
Objective: Set up a Python virtual environment and install dependencies.
Steps:
1. Create a virtual environment:
bash:
```
python3 -m venv venv
```

2. Activate the virtual environment and install dependencies:
bash:
```
source venv/bin/activate
pip install -r requirements.txt
```

Jenkinsfile snip:
```
stage('Install Dependencies') {
    steps {
        script {
            if (isUnix()) {
                sh './venv/bin/activate'
            } else {
                bat 'venv\\Scripts\\activate'
            }
            sh 'pip install -r requirements.txt'
        }
    }
}
```

## Stage 2: Run Migrations
Objective: Apply database migrations to ensure that the database schema is up-to-date.

Steps:
1. Run the migration commands:
Jenkinsfile snip:
```
stage('Run Migrations') {
            steps {
                script {
                    // Apply database migrations using the python executable from the virtual environment
                    sh './venv/bin/python3 manage.py migrate'
                }
            }
        }
```

## Stage 3: Run Tests
Objective: Execute Django tests to verify that the application works as expected and to catch any issues early.

Steps:
1. Start the Django development server in the background:

bash:
```
nohup ./venv/bin/python manage.py runserver 0.0.0.0:8000 &
```
Wait for the server to start:

bash:
```
sleep 10
```
Run a smoke test to check if the server is running:

bash:
```
curl -f http://localhost:8000 || exit 1
```
Kill the Django development server:

bash:
```
pkill -f runserver
```

Jenkinsfile snip:
```
stage('Run Tests') {
    steps {
        script {
            sh 'nohup ./venv/bin/python manage.py runserver 0.0.0.0:8000 &'
            sh 'sleep 10'
            sh 'curl -f http://localhost:8000 || exit 1'
            sh 'pkill -f runserver'
        }
    }
}
```

## Stage 4: Static Analysis
Objective: Perform static code analysis to maintain code quality and style consistency.

Steps:

Run static analysis script:
bash:
```
./static_scan.sh
```
Jenkinsfile snip:
```
stage('Static Analysis') {
    steps {
        script {
            sh './static_scan.sh'
        }
    }
}
```

## Stage 5: Build and Archive
Objective: Package the project files and archive them for future use.

Steps:
Create a build directory and copy project files:
bash:
```
mkdir -p build
cp -r ssm_app/ ssm_project/ manage.py requirements.txt build/
tar -czf build.tar.gz -C build .
```
Archive the build artifact:
Archive the build.tar.gz using Jenkins
Jenkinsfile snip:
```
stage('Build and Archive') {
    steps {
        script {
            sh '''
                mkdir -p build
                cp -r ssm_app/ ssm_project/ manage.py requirements.txt build/
                tar -czf build.tar.gz -C build .
            '''
        }
        archiveArtifacts artifacts: 'build.tar.gz', followSymlinks: false
    }
}
```

## Stage 6: Build Docker Image
Objective: Build a Docker image for the Django application.

Steps:
Ensure the Dockerfile is in the correct location and build the Docker image:
bash:
```
docker build -t ssilviu11/django_project:latest .
docker images
```
Jenkinsfile snip:
```
stage('Build Docker Image') {
    steps {
        script {
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
```

Stage 7: Publish Docker Image
Objective: Push the Docker image to Docker Hub for distribution and deployment.
Steps:

Log in to Docker Hub and push the image:
bash:
```
docker login -u $DOCKER_USER -p $DOCKER_PASS
docker tag ssilviu11/django_project:latest ssilviu11/django_project:latest
docker push ssilviu11/django_project:latest
```

Jenkinsfile snip:
```
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
```

## Stage 8: Deploy Container and Test
Objective: Deploy the Docker container locally for testing and verification.

Steps:
Run the Docker container:
bash:
```
docker run -d -p 4000:8000 --name app ssilviu11/django_project:latest
sleep 10
docker ps -a
docker logs app
curl -f http://localhost:4000 || exit 1
```
Jenkinsfile snip:
```
stage('Deploy Container and Test') {
    steps {
        script {
            sh '''
                docker run -d -p 4000:8000 --name app ssilviu11/django_project:latest
                sleep 10
                docker ps -a
                docker logs app
                curl -f http://localhost:4000 || exit 1
            '''
        }
    }
}
```

## Stage 9: Clean-up Containers and Images
Objective: Remove any stopped containers and unused Docker images to free up space.

Steps:
Clean up containers and images:
bash:
```
if docker container ls -a | grep app ; then
    docker container stop app
    docker container rm app
fi

if docker image ls -a | grep ssilviu11/django_project ; then
    docker image rm ssilviu11/django_project:latest
fi
```
Jenkinsfile snip:
```
stage('Clean-up Containers and Images') {
    steps {
        script {
            sh '''
                if docker container ls -a | grep app ;
                then
                    docker container stop app
                    docker container rm app
                fi

                if docker image ls -a | grep ssilviu11/django_project ;
                then
                    docker image rm ssilviu11/django_project:latest
                fi
            '''
        }
    }
}
```

## Running the Pipeline
To run the Jenkins pipeline, follow these steps:

Access Jenkins Dashboard: Open your Jenkins dashboard in a web browser.
Select the Job: Click on the job linked to your project.
**Build Now





