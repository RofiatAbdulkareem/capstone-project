from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Importing task functions from the tasks folder
from tasks.extract_to_s3 import extract_data
from tasks.transform import transform_data
from tasks.write_to_warehouse import write_to_warehouse

# Default arguments for the DAG
default_args = {
    "owner": "Rofiat",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": False,
    "email_on_retry": False,
}

# Define the DAG
with DAG(
    dag_id="travel_agency_pipeline",
    default_args=default_args,
    description="ETL pipeline for travel agency data",
    schedule_interval="@daily",  # You can modify this as per your need
    start_date=datetime(2024, 11, 1),
    catchup=False,
    tags=["travel_agency", "ETL"],
) as dag:

    # Task 1: Extract raw data from API and upload to S3
    extract_task = PythonOperator(
        task_id="extract_raw_data",
        python_callable=extract_data,
        # Pass any necessary arguments to extract_data function
    )

    # Task 2: Transform raw data and upload data to S3 
    transform_task = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data,
        # Pass the output from extract_task as input if necessary
    )

    # Task 3: Write processed data to Postgres
    write_to_warehouse_task = PythonOperator(
        task_id="load_to_warehouse",
        python_callable=write_to_warehouse,
        # Pass the processed data from transform_task as input if needed
    )

    # Set task dependencies
    extract_task >> transform_task >> write_to_warehouse_task
