# 🚀 Jenkins CI/CD Hands-On Project

A complete hands-on project demonstrating Jenkins CI/CD pipelines with Docker, featuring a **Frontend** (HTML/CSS/JS + Nginx) and **Backend** (Python Flask) application.

---

## 📋 Table of Contents

1. [Project Overview](#-project-overview)
2. [Project Structure](#-project-structure)
3. [Prerequisites](#-prerequisites)
4. [Part 1: Jenkins Setup on EC2](#-part-1-jenkins-setup-on-ec2)
5. [Part 2: Docker Configuration](#-part-2-docker-configuration)
6. [Part 3: Create Jenkins Pipelines](#-part-3-create-jenkins-pipelines)
7. [Part 4: Run the Pipelines](#-part-4-run-the-pipelines)
8. [Local Development](#-local-development)
9. [Pipeline Features](#-pipeline-features)
10. [Troubleshooting](#-troubleshooting)

---

## 🎯 Project Overview

This project includes:

| Component | Technology | Description |
|-----------|------------|-------------|
| **Frontend** | HTML, CSS, JS, Nginx | Modern static website with API integration |
| **Backend** | Python Flask | RESTful API with health checks |
| **Pipelines** | Jenkins | 2 separate pipelines with multi-agent setup |
| **Containers** | Docker | Dockerized applications |

---

## 📁 Project Structure

```
Jenkins-CICD/
├── frontend/
│   ├── index.html          # Main HTML file
│   ├── styles.css          # CSS styling
│   ├── app.js              # JavaScript logic
│   ├── Dockerfile          # Frontend Docker config
│   └── nginx.conf          # Nginx configuration
├── backend/
│   ├── app.py              # Flask application
│   ├── requirements.txt    # Python dependencies
│   ├── test_app.py         # Unit tests
│   └── Dockerfile          # Backend Docker config
├── Jenkinsfile-frontend    # Pipeline for frontend
├── Jenkinsfile-backend     # Pipeline for backend
├── docker-compose.yml      # Local development
├── .gitignore
└── README.md
```

---

## ✅ Prerequisites

Before starting, ensure you have:

- [ ] AWS Account with EC2 access
- [ ] GitHub account (to host this repository)
- [ ] Docker Hub account (for pushing images)
- [ ] Basic understanding of Docker and Jenkins

---

## 🔧 Part 1: Jenkins Setup on EC2

### Step 1.1: Launch EC2 Instance

1. Go to **AWS Console** → **EC2** → **Launch Instance**
2. Configure:
   - **Name**: `jenkins-server`
   - **AMI**: Ubuntu Server 22.04 LTS
   - **Instance Type**: t2.medium (recommended) or t2.micro
   - **Key Pair**: Create or select existing
   - **Security Group**: Allow ports 22, 8080, 80, 5000

### Step 1.2: Connect to EC2

```bash
ssh -i your-key.pem ubuntu@<EC2-PUBLIC-IP>
```

### Step 1.3: Install Java

```bash
sudo apt update
sudo apt install openjdk-17-jre -y
java -version
```

### Step 1.4: Install Jenkins

```bash
# Add Jenkins repository key
curl -fsSL https://pkg.jenkins.io/debian/jenkins.io-2023.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null

# Add Jenkins repository
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null

# Install Jenkins
sudo apt-get update
sudo apt-get install jenkins -y
```

### Step 1.5: Start Jenkins

```bash
sudo systemctl start jenkins
sudo systemctl enable jenkins
sudo systemctl status jenkins
```

### Step 1.6: Access Jenkins

1. Open browser: `http://<EC2-PUBLIC-IP>:8080`
2. Get initial password:
   ```bash
   sudo cat /var/lib/jenkins/secrets/initialAdminPassword
   ```
3. Install suggested plugins
4. Create admin user

---

## 🐳 Part 2: Docker Configuration

### Step 2.1: Install Docker

```bash
sudo apt update
sudo apt install docker.io -y
```

### Step 2.2: Configure Permissions

```bash
sudo usermod -aG docker jenkins
sudo usermod -aG docker ubuntu
sudo systemctl restart docker
```

### Step 2.3: Restart Jenkins

```bash
sudo systemctl restart jenkins
```

Or visit: `http://<EC2-PUBLIC-IP>:8080/restart`

### Step 2.4: Install Jenkins Plugins

1. Go to **Manage Jenkins** → **Manage Plugins**
2. Install these plugins:
   - Docker Pipeline
   - Docker
   - Pipeline
   - Git
   - GitHub Integration

### Step 2.5: Configure Docker Hub Credentials

1. Go to **Manage Jenkins** → **Manage Credentials**
2. Click **System** → **Global credentials** → **Add Credentials**
3. Configure:
   - **Kind**: Username with password
   - **ID**: `docker-hub-credentials`
   - **Username**: Your Docker Hub username
   - **Password**: Your Docker Hub password/token

---

## 🔨 Part 3: Create Jenkins Pipelines

### Step 3.1: Push Code to GitHub

```bash
# Initialize git repository
cd Jenkins-CICD
git init
git add .
git commit -m "Initial commit: Jenkins CI/CD demo project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/Jenkins-CICD.git
git push -u origin main
```

### Step 3.2: Create Frontend Pipeline

1. **Jenkins Dashboard** → **New Item**
2. Enter name: `frontend-pipeline`
3. Select: **Pipeline**
4. Click **OK**

5. Configure Pipeline:
   - **Definition**: Pipeline script from SCM
   - **SCM**: Git
   - **Repository URL**: `https://github.com/YOUR_USERNAME/Jenkins-CICD.git`
   - **Branch**: `*/main`
   - **Script Path**: `Jenkinsfile-frontend`

6. Click **Save**

### Step 3.3: Create Backend Pipeline

1. **Jenkins Dashboard** → **New Item**
2. Enter name: `backend-pipeline`
3. Select: **Pipeline**
4. Click **OK**

5. Configure Pipeline:
   - **Definition**: Pipeline script from SCM
   - **SCM**: Git
   - **Repository URL**: `https://github.com/YOUR_USERNAME/Jenkins-CICD.git`
   - **Branch**: `*/main`
   - **Script Path**: `Jenkinsfile-backend`

6. Click **Save**

---

## ▶️ Part 4: Run the Pipelines

### Step 4.1: Update Jenkinsfiles

Before running, update the Docker image names in both Jenkinsfiles:

**Jenkinsfile-frontend (line 16):**
```groovy
DOCKER_IMAGE_NAME = 'YOUR_DOCKERHUB_USERNAME/frontend-app'
```

**Jenkinsfile-backend (line 14):**
```groovy
DOCKER_IMAGE_NAME = 'YOUR_DOCKERHUB_USERNAME/backend-app'
```

Commit and push changes:
```bash
git add .
git commit -m "Update Docker Hub username"
git push origin main
```

### Step 4.2: Run Backend Pipeline

1. Go to `backend-pipeline`
2. Click **Build Now**
3. Watch the pipeline stages execute:
   - ✅ Checkout
   - ✅ Install Dependencies
   - ✅ Code Quality
   - ✅ Run Tests
   - ✅ Build Docker Image
   - ✅ Test Docker Image
   - ✅ Push to Registry (main branch only)
   - ✅ Deploy (main branch only)

### Step 4.3: Run Frontend Pipeline

1. Go to `frontend-pipeline`
2. Click **Build Now**
3. Watch the pipeline stages execute:
   - ✅ Checkout
   - ✅ Build & Validate
   - ✅ Docker Build
   - ✅ Test Docker Image
   - ✅ Push to Registry (main branch only)
   - ✅ Deploy (main branch only)

### Step 4.4: Verify Deployment

After successful deployment, access your applications:

- **Frontend**: `http://<EC2-PUBLIC-IP>/`
- **Backend**: `http://<EC2-PUBLIC-IP>:5000/api/health`

---

## 💻 Local Development

### Run with Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Access Applications

- **Frontend**: http://localhost
- **Backend**: http://localhost:5000

### Test Backend Locally

```bash
cd backend
pip install -r requirements.txt
pytest test_app.py -v
```

---

## ⚡ Pipeline Features

### Frontend Pipeline (`Jenkinsfile-frontend`)

| Stage | Agent | Description |
|-------|-------|-------------|
| Checkout | any | Clone source code |
| Build & Validate | Docker (node:18) | Validate HTML/CSS/JS |
| Docker Build | any | Build Docker image |
| Test Docker Image | any | Run container tests |
| Push to Registry | any | Push to Docker Hub |
| Deploy | any | Deploy container |

### Backend Pipeline (`Jenkinsfile-backend`)

| Stage | Agent | Description |
|-------|-------|-------------|
| Checkout | any | Clone source code |
| Install Dependencies | Docker (python:3.11) | Install Python packages |
| Code Quality | Docker (python:3.11) | Run flake8, black |
| Run Tests | Docker (python:3.11) | Run pytest with coverage |
| Build Docker Image | any | Build Docker image |
| Security Scan | any | Placeholder for security tools |
| Test Docker Image | any | API endpoint tests |
| Push to Registry | any | Push to Docker Hub |
| Deploy | any | Deploy container |

---

## 🔍 Troubleshooting

### Docker Permission Denied

```bash
sudo chmod 666 /var/run/docker.sock
sudo systemctl restart jenkins
```

### Jenkins Can't Connect to Docker

```bash
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

### Port Already in Use

```bash
# Check what's using the port
sudo lsof -i :8080
sudo lsof -i :5000

# Kill the process
sudo kill -9 <PID>
```

### View Container Logs

```bash
docker logs cicd-frontend
docker logs cicd-backend
```

---

## 📚 Additional Resources

- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [Docker Documentation](https://docs.docker.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

## 🎉 Congratulations!

You have successfully set up:
- ✅ Jenkins on EC2
- ✅ Docker as Jenkins agent
- ✅ Two CI/CD pipelines with multi-agent setup
- ✅ Containerized frontend and backend applications

**Happy Learning! 🚀**
