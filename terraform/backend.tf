terraform {
  backend "s3" {
    bucket       = "terraformstate24072026"
    key          = "eks/dev/terraform.tfstate"
    region       = "us-east-1"
    use_lockfile = true
    encrypt      = true
  }
}
