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

