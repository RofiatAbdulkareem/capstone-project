output "s3_bucket_name" {
  value = aws_s3_bucket.raw_data_bucket.bucket
}

output "rds_endpoint" {
  value = aws_db_instance.data_warehouse.endpoint
}

output "iam_role_arn" {
  value = aws_iam_role.airflow_role.arn
}
