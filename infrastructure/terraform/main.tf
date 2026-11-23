terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region  = "us-east-2"
  profile = "portfolio"
}

resource "aws_dynamodb_table" "visitor_counter" {
  name         = "PortfolioVisitorCounter"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"
  table_class  = "STANDARD"

  deletion_protection_enabled = false

  attribute {
    name = "id"
    type = "S"
  }

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_lambda_function" "visitor_counter" {
  function_name = "PortfolioVisitorCounterFunction"
  filename      = "${path.module}/../../backend/portfolio-lambda.zip"

  role = "arn:aws:iam::729005488068:role/service-role/PortfolioVisitorCounterFunction-role-qvcljxfc"

  runtime = "python3.14"
  handler = "lambda_function.lambda_handler"

  timeout       = 3
  memory_size   = 128
  architectures = ["x86_64"]

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.visitor_counter.name
    }
  }

  lifecycle {
    prevent_destroy = true

    ignore_changes = [
      filename,
      source_code_hash,
      s3_bucket,
      s3_key,
      s3_object_version
    ]
  }
}