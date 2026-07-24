module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.24"

  cluster_name    = var.cluster_name
  cluster_version = var.cluster_version

  vpc_id     = var.vpc_id
  subnet_ids = var.subnet_ids

  #################################################
  # We already created IAM roles
  #################################################

  create_iam_role = false
  iam_role_arn    = var.cluster_role_arn

  #################################################
  # EKS API Endpoint
  #################################################

  # Makes the Kubernetes API server accessible over the internet.
  # This allows kubectl, Helm, and GitHub Actions running outside
  # the VPC to connect to and manage the EKS cluster.
  cluster_endpoint_public_access = true

  #################################################
  # Authentication
  #################################################

  # Enables both the new EKS Access Entry API and the traditional
  # aws-auth ConfigMap for IAM authentication.
  # This allows IAM users and roles to authenticate to the cluster.
  authentication_mode = "API_AND_CONFIG_MAP"

  #################################################
  # IAM Roles for Service Accounts (IRSA)
  #################################################

  # Enables IRSA, allowing Kubernetes Service Accounts to assume
  # dedicated IAM roles. This gives individual pods least-privilege
  # access to AWS services (such as S3, DynamoDB, or Secrets Manager)
  # instead of using the worker node's IAM role.
  enable_irsa = true

  #################################################
  # We'll create node groups separately
  #################################################

  access_entries = {
    admin = {
      principal_arn = "arn:aws:iam::416772749198:user/NamanGarg"

      policy_associations = {
        admin = {
          policy_arn = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy"

          access_scope = {
            type = "cluster"
          }
        }
      }
    }
  }

  #It won't scale automatically because I haven't installed Cluster Autoscaler or Karpenter. 
  #The values desired_size, min_size, and max_size only define the allowed range of nodes.

  eks_managed_node_groups = {

    default = {
      name            = "default"
      create_iam_role = false
      iam_role_arn    = var.node_role_arn

      instance_types = ["t3.small"]

      ami_type = "AL2023_x86_64_STANDARD"

      desired_size = 1
      min_size     = 1
      max_size     = 2

      disk_size = 30

      capacity_type = "ON_DEMAND"

      labels = {
        role = "worker"
      }

      update_config = {
        max_unavailable_percentage = 25
      }

      tags = {
        Name = "default-node-group"
      }
    }
  }

  tags = {
    Terraform = "true"
  }
}

