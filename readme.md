# Flask SRE Assessment Project

This repository contains a simple Flask application, Kubernetes deployment assets, Terraform infrastructure code, and GitHub Actions pipelines for CI/CD and infrastructure provisioning.

## What is included

- Flask application with health, readiness, and version endpoints
- Docker image build for the application
- Helm chart for deploying to Kubernetes
- Terraform modules for AWS infrastructure provisioning
- GitHub Actions workflows for:
  - application CI/CD
  - Terraform plan/apply

## Project structure

- app/: Flask application source, tests, Dockerfile, Python dependencies
- helm/flask-app/: Helm chart for the application deployment
- terraform/: Terraform modules and environment configuration
- .github/workflows/: GitHub Actions pipelines

## Prerequisites

Before running locally, make sure you have:

- Python 3.12+
- pip
- Docker
- kubectl
- Helm
- Terraform
- Access to an AWS account with permissions for ECR, EKS, and IAM

## Local setup

### 1. Clone and enter the repository

```bash
git clone <repository-url>
cd testRepo
```

### 2. Set up the Python environment

```bash
cd app
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows PowerShell
pip install -r requirements-dev.txt
```

### 3. Run the application locally

```bash
python app.py
```

The app will be available at:

- http://localhost:5000/
- http://localhost:5000/health
- http://localhost:5000/ready
- http://localhost:5000/version

### 4. Run tests

```bash
pytest --cov=. --cov-report=xml
```

### 5. Build the Docker image locally

```bash
docker build -t flask-app:local .
```

### 6. Deploy locally with Helm

```bash
helm install flask-app ./helm/flask-app \
  --set image.repository=flask-app \
  --set image.tag=local
```

## GitHub Actions pipelines

### Application pipeline

The workflow in .github/workflows/app-ci-cd.yml runs on pushes to main when files under app/ or helm/ change.

It performs:

- Python dependency installation
- formatting checks with Black and isort
- linting with Flake8 and Pylint
- unit tests with pytest and coverage reporting
- SonarCloud scanning
- Docker build and push to ECR
- Helm deployment to EKS

### Terraform pipeline

The workflow in .github/workflows/terraform.yml runs on pushes to the main branch when Terraform files change, and can also be started manually.

It performs:

- Terraform fmt validation
- terraform init
- terraform validate
- terraform plan
- terraform apply on the main branch

## Required GitHub secrets

The workflows expect these repository secrets:

- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_REGION
- EKS_CLUSTER_NAME
- ECR_REPOSITORY
- SONAR_TOKEN

