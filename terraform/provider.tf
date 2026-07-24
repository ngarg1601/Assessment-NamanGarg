provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "sre-assessment"
      Environment = var.environment
      ManagedBy   = "TerraformCode"
    }
  }
}
