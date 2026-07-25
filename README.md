Cyber Threat Detection API (MLOps)
Overview
This repository contains a machine learning operations (MLOps) pipeline designed to classify network threats. The application is built using a FastAPI backend and is containerized with Docker. Infrastructure is provisioned on AWS as Infrastructure as Code (IaC) using Terraform.

Architecture & Technology Stack
Application Framework: Python / FastAPI

Containerization: Docker

Cloud Provider: AWS (EC2 t3.micro instances, Ubuntu AMI)

Infrastructure Provisioning: Terraform

Orchestration (Planned): Kubernetes

Project Structure
Plaintext
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── model/               # Threat classification models and logic
│   └── requirements.txt     # Python dependencies
├── infrastructure/
│   └── terraform/
│       ├── main.tf          # AWS EC2 and networking configuration
│       ├── variables.tf     # Terraform input variables
│       └── outputs.tf       # Terraform outputs (e.g., Public IP)
├── Dockerfile               # Container build instructions
├── .gitignore               # Ignored files (Terraform state, env vars, pycache)
└── README.md
Prerequisites
To deploy and run this project, ensure you have the following installed locally:

Git

Terraform

AWS CLI (Configured with appropriate credentials)

Docker

Infrastructure Deployment
The infrastructure is managed via Terraform and deployed to the ca-central-1 (Canada Central) AWS region.

Navigate to the Terraform directory:

Bash
cd infrastructure/terraform
Initialize the Terraform workspace:

Bash
terraform init
Review the deployment plan:

Bash
terraform plan
Apply the configuration to provision the AWS server:

Bash
terraform apply
Retrieve the newly generated public IP address:

Bash
terraform state show aws_instance.mlops_server | grep public_ip
Server Configuration & Application Deployment
Once the EC2 instance is running, connect via SSH or EC2 Instance Connect to deploy the application.

Install Docker on the Ubuntu Server:

Bash
sudo apt update
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu
newgrp docker
Clone the Repository:

Bash
git clone <YOUR_REPOSITORY_URL>
cd <PROJECT_FOLDER_NAME>
Build the Docker Image:

Bash
docker build -t threat-classifier-api .
Run the Container:

Bash
docker run -d -p 8000:8000 threat-classifier-api
The API will now be accessible at http://<EC2_PUBLIC_IP>:8000.

Future Scope (Phase 3)
Push the compiled Docker image to a central container registry (e.g., Docker Hub or AWS ECR).

Deploy a Kubernetes cluster to orchestrate the containers.

Implement deployment.yaml and service.yaml manifests for internal networking and pod replication.
