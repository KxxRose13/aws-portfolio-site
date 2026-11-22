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