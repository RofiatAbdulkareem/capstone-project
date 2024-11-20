variable "region" {
  default = "us-east-1"
}

variable "s3_bucket_name" {
  default = "cde-travel-data-lake"
}

variable "db_instance_class" {
  default = "db.t3.micro"
}

variable "db_name" {
  default = "travel_agency_dw"
}

variable "db_username" {
  default = "admin"
}
