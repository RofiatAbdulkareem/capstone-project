# 1. S3 Bucket for Raw Data
resource "aws_s3_bucket" "raw_data_bucket" {
  bucket = "cde-travel-data-lake" # Name of the bucket

  tags = {
    Name        = "CDE Travel Data Lake"
    Environment = "Dev"
  }
}

# 2. IAM Role for Airflow
resource "aws_iam_role" "airflow_role" {
  name = "AirflowETLRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
      Action = "sts:AssumeRole"
    }]
  })
}

# 3. IAM Policy for S3 and SSM Access
resource "aws_iam_role_policy" "airflow_policy" {
  name   = "AirflowPolicy"
  role   = aws_iam_role.airflow_role.name
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect: "Allow"
        Action: [
          "s3:*"
        ]
        Resource: "*"
      },
      {
        Effect: "Allow"
        Action: [
          "ssm:GetParameter",
          "ssm:GetParameters"
        ]
        Resource: "arn:aws:ssm:us-east-1:123456789012:parameter/travel-agency-warehousepassword" 
      }
    ]
  })
}

# 4. Retrieve the RDS Password from SSM Parameter Store
data "aws_ssm_parameter" "db_password" {
  name = "travel-agency-warehousepassword" # Name of the existing SSM parameter
}

# 5. RDS (PostgreSQL) Database for Data Warehouse
resource "aws_db_instance" "data_warehouse" {
  allocated_storage    = 20
  engine               = "postgres"
  engine_version       = "15.7"
  instance_class       = "db.t3.micro"
  db_name              = "travel_agency_dw"
  username             = "rofee"
  password             = data.aws_ssm_parameter.db_password.value
  publicly_accessible  = true
  skip_final_snapshot  = true

  tags = {
    Name        = "Travel Agency Data Warehouse"
    Environment = "Dev"
  }
}