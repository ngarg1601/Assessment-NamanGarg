#############################################
# VPC 
#############################################

module "vpc" {
  source = "./modules/vpc"

  name        = var.cluster_name
  environment = var.environment
  aws_region  = var.aws_region
  vpc_cidr    = var.vpc_cidr
}

#############################################
# IAM
#############################################

module "iam" {
  source = "./modules/iam"

  cluster_name = var.cluster_name
}

#############################################
# EKS Cluster
#############################################

module "eks" {
  source = "./modules/eks"

  cluster_name    = var.cluster_name
  cluster_version = var.cluster_version

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  cluster_role_arn = module.iam.cluster_role_arn
  node_role_arn    = module.iam.node_role_arn
}

#############################################
# ECR
#############################################

module "ecr" {
  source = "./modules/ecr"

  repository_name = var.repository_name
  environment     = var.environment
}
