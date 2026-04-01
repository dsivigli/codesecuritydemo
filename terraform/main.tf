
# VULNERABILITY: Security group with overly permissive rules
resource "aws_security_group" "app_sg" {
  name        = "vulnerable-app-sg"
  description = "Security group for vulnerable Flask app"

  # VULNERABILITY: Allow all inbound traffic
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # VULNERABILITY: Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# VULNERABILITY: EC2 instance with public IP and SSH access
resource "aws_instance" "app_server" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  
  # VULNERABILITY: Public IP exposed
  associate_public_ip_address = true
  
  vpc_security_group_ids = [aws_security_group.app_sg.id]
  
  # VULNERABILITY: Storing SSH key in user_data
  user_data = <<-EOF
              #!/bin/bash
              echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQD3F6tyPEFEzV0LX3X8BsXdMsQz1x2cEikKDEY0aIj41qgxMCP/iteneqXSIFZBp5vizPvaoIR3Um9xK7PGoW8giupGn+EPuxIA4cDM4vzOqOkiMPhz5XK0whEjkVzTo4+S0puvDZuwIsdiW9mxhJc7tgBNL0cYlWSYVkz4G/fslNfRPW5mYAM49f4fhtxPb5ok4Q2Lg9dPKVHO/Bgeu5woMc7RY0p1ej6D4CKFE6lymSDJpW0YHX/wqE9+cfEauh7xZcG0q9t2ta6F6fmX0agvpFyZo8aFbXeUBr7osSCJNgvavWbM/06niWrOvYX2xwWdhXmXSrbX8ZbabVohBK41 insecure@example.com" >> /home/ec2-user/.ssh/authorized_keys
              EOF
  
  # VULNERABILITY: No encryption for EBS volumes
  root_block_device {
    volume_size = 10
    encrypted   = false
  }
  
  tags = {
    Name = "VulnerableAppServer"
  }
}

# VULNERABILITY: RDS instance with public access
resource "aws_db_instance" "app_db" {
  allocated_storage    = 10
  engine               = "mysql"
  engine_version       = "5.7"
  instance_class       = "db.t2.micro"
  name                 = "vulnerable_db"
  username             = "admin"
  # VULNERABILITY: Hardcoded database password
  password             = "insecure_password"
  parameter_group_name = "default.mysql5.7"
  # VULNERABILITY: Publicly accessible database
  publicly_accessible  = true
  # VULNERABILITY: No encryption at rest
  storage_encrypted    = false
  # VULNERABILITY: No deletion protection
  deletion_protection  = false
  # VULNERABILITY: No multi-AZ deployment
  multi_az             = false
  # VULNERABILITY: Skip final snapshot
  skip_final_snapshot  = true
}

# VULNERABILITY: IAM user with admin privileges
resource "aws_iam_user" "app_user" {
  name = "vulnerable-app-user"
}

# VULNERABILITY: IAM policy with excessive permissions
resource "aws_iam_user_policy" "app_user_policy" {
  name = "vulnerable-app-policy"
  user = aws_iam_user.app_user.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = "*"
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}

# VULNERABILITY: Hardcoded access keys
resource "aws_iam_access_key" "app_user_key" {
  user = aws_iam_user.app_user.name
}


