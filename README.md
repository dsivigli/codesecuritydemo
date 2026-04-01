# Flask Web Application with AWS Infrastructure

## Overview

This project is a Python Flask web application designed for deployment on AWS infrastructure. The application provides a simple web interface and is automatically deployed using Infrastructure as Code (IaC) principles with comprehensive monitoring and continuous deployment capabilities.

## Application Architecture

### Core Application
- **Framework**: Python Flask web framework
- **Runtime**: Python 3.x
- **Web Server**: Built-in Flask development server
- **Port**: 5001
- **Interface**: Web-based user interface with HTML templates

### AWS Infrastructure Components

#### Compute & Networking
- **EC2 Instance**: t2.micro Amazon Linux 2 instance
- **VPC**: Custom Virtual Private Cloud with public subnet
- **Security Groups**: Configured for web traffic and SSH access
- **Internet Gateway**: Direct internet connectivity
- **Public IP**: Automatically assigned for external access

#### Storage & Content Delivery
- **S3 Bucket**: Centralized storage for application files
- **Application Structure**: Organized in `application/` folder within S3
- **Automatic Sync**: Real-time synchronization between S3 and EC2

#### Monitoring & Observability
- **CloudWatch Agent**: Comprehensive system and application monitoring
- **Metrics Collection**: CPU, memory, disk usage, and network statistics
- **Log Aggregation**: System logs centralized in CloudWatch Logs
- **Custom Dashboards**: Real-time performance monitoring

#### Automation & Deployment
- **Lambda Functions**: Serverless automation for deployment tasks
- **SSM Documents**: Standardized system configuration and software installation
- **Custom Resources**: CloudFormation-managed deployment triggers
- **S3 Event Triggers**: Automatic application updates on file changes

## Technologies Used

### Application Stack
- **Python 3**: Primary programming language
- **Flask**: Lightweight web application framework
- **Jinja2**: Template engine for dynamic HTML generation
- **HTML/CSS**: Frontend presentation layer

### AWS Services
- **Amazon EC2**: Virtual server hosting
- **Amazon VPC**: Network isolation and security
- **Amazon S3**: Object storage and static file hosting
- **AWS Lambda**: Serverless compute for automation
- **Amazon CloudWatch**: Monitoring and logging
- **AWS Systems Manager (SSM)**: Configuration management
- **AWS CloudFormation**: Infrastructure as Code deployment
- **AWS IAM**: Identity and access management

### DevOps & CI/CD
- **GitLab CI/CD**: Continuous integration and deployment pipeline
- **AWS CLI**: Command-line interface for AWS operations
- **CloudFormation Templates**: YAML-based infrastructure definitions
- **Automated Testing**: Code validation and deployment verification

## Key Features

### Automated Deployment
- **One-Click Infrastructure**: Complete AWS environment provisioning via CloudFormation
- **Application Deployment**: Automated Flask application setup and configuration
- **Dependency Management**: Automatic Python package installation
- **Service Management**: Systemd service configuration for application lifecycle

### Continuous Integration
- **Code Validation**: Automated Python syntax and dependency checking
- **S3 Synchronization**: Automatic file uploads to S3 on code changes
- **Zero-Downtime Updates**: Rolling updates triggered by S3 file changes
- **Pipeline Automation**: GitLab CI/CD integration for seamless deployments

### Monitoring & Maintenance
- **Real-Time Metrics**: System performance monitoring via CloudWatch
- **Log Centralization**: Application and system logs in CloudWatch Logs
- **Health Monitoring**: Automated service health checks and recovery
- **Performance Tracking**: CPU, memory, disk, and network utilization

### Scalability & Management
- **Infrastructure as Code**: Version-controlled infrastructure definitions
- **Parameterized Deployment**: Configurable S3 bucket names and regions
- **Resource Tagging**: Organized resource management and cost tracking
- **Security Groups**: Network-level access control and traffic filtering

## Deployment Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   GitLab CI/CD  │───▶│   Amazon S3      │───▶│  Lambda Trigger │
│   Pipeline      │    │   Bucket         │    │  Function       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  CloudFormation │    │   EC2 Instance   │◀───│  SSM Command    │
│  Template       │───▶│   Flask App      │    │  Execution      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │  CloudWatch      │
                       │  Monitoring      │
                       └──────────────────┘
```

## Getting Started

### Prerequisites
- AWS Account with appropriate permissions
- GitLab account for CI/CD pipeline
- AWS CLI configured with credentials
- S3 bucket for application storage

### Deployment Steps
1. **Configure GitLab Variables**: Set `S3_BUCKET_NAME` in GitLab project settings
2. **Deploy Infrastructure**: Run CloudFormation template deployment
3. **Upload Application**: Push code changes to trigger CI/CD pipeline
4. **Access Application**: Use the provided EC2 public IP and port 5001

### Configuration
- **S3 Bucket**: Must be globally unique and accessible from your AWS account
- **Region**: Default deployment region is us-east-1
- **Instance Type**: t2.micro (suitable for development and testing)
- **Network**: Public subnet with internet gateway for external access

## Monitoring & Maintenance

The application includes comprehensive monitoring through CloudWatch:
- **System Metrics**: CPU, memory, disk usage automatically collected
- **Application Logs**: Centralized logging for troubleshooting
- **Performance Dashboards**: Real-time system performance visualization
- **Automated Alerts**: Configurable thresholds for proactive monitoring

## Support & Documentation

For technical support and detailed configuration options, refer to the CloudFormation template parameters and GitLab CI/CD pipeline configuration. The infrastructure is designed to be self-documenting through comprehensive resource tagging and output values.