terraform {
  backend "s3" {
    bucket         = "terraform-state-cde"
    key            = "state/terraform.tfstate"
    region         = "us-east-1"
  }
}
