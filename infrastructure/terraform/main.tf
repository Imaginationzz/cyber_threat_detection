provider "aws" {
  region = "ca-central-1" 
}

# 1. Find the latest Ubuntu machine image
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Official Canonical Ubuntu account ID

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

# 2. DevSecOps: The Security Group (Firewall)
resource "aws_security_group" "mlops_sg" {
  name        = "mlops-threat-classifier-sg"
  description = "Allow inbound traffic for Kubernetes and FastAPI"

  ingress {
    description = "HTTPS for web traffic"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "FastAPI Application Port"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH Access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] 
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1" # Allows all outbound traffic so the server can download updates
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# 3. The actual EC2 Virtual Server
resource "aws_instance" "mlops_server" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.small" # Minimum size recommended to comfortably run Kubernetes

  vpc_security_group_ids = [aws_security_group.mlops_sg.id]

  tags = {
    Name = "Threat-Classifier-K8s-Node"
  }
}