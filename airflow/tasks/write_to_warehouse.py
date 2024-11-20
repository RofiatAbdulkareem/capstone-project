import pandas as pd
import boto3
from sqlalchemy import create_engine
import io
import re

def write_to_warehouse():
    """
    Reads transformed data from an S3 bucket and writes it to a PostgreSQL database.
    """
    # AWS S3 and SSM clients
    s3_client = boto3.client('s3')
    ssm_client = boto3.client('ssm', region_name='us-east-1')

    # Define S3 bucket and file details
    bucket_name = 'cde-travel-data-lake'
    file_key = 'transform/countries_data_transformed.parquet'

    # Retrieve the RDS password from SSM Parameter Store
    parameter_name = 'travel-agency-warehousepassword'
    try:
        rds_password = ssm_client.get_parameter(Name=parameter_name, WithDecryption=True)['Parameter']['Value']
    except Exception as e:
        print(f"Error retrieving RDS password: {e}")
        raise

    # Read the Parquet file from S3
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        df_transformed = pd.read_parquet(io.BytesIO(response['Body'].read()))
    except Exception as e:
        print(f"Error reading file from S3: {e}")
        raise

    # Ensure all string columns are WIN1252 compatible
    for col in df_transformed.select_dtypes(include=['object']).columns:
        df_transformed[col] = df_transformed[col].apply(
            lambda x: (
                x.encode('latin1', errors='ignore').decode('latin1') if isinstance(x, str) else x
            )
        )

    # Database connection parameters
    db_user = 'rofee'
    db_host = 'terraform-20241113122124605100000001.cz4qw448wzk4.us-east-1.rds.amazonaws.com'
    db_port = '5432'
    db_name = 'travel_agency_dw'

    # Create the connection string
    connection_string = f'postgresql+psycopg2://{db_user}:{rds_password}@{db_host}:{db_port}/{db_name}'

    # Create the SQLAlchemy engine
    engine = create_engine(connection_string)

    # Load the data into a table in your RDS PostgreSQL
    try:
        # Check if the connection works
        with engine.connect() as connection:
            print("Connection to RDS PostgreSQL successful.")

        # Ensure the table name is appropriate
        table_name = 'transformed_data'

        # Pass the engine directly to to_sql
        df_transformed.to_sql(
            name=table_name, con=engine, if_exists='replace', index=False
        )
        print(f"Data successfully loaded into the '{table_name}' table in PostgreSQL.")
    except Exception as e:
        print(f"An error occurred while writing to the warehouse: {e}")
        raise
    finally:
        engine.dispose()  # Close the connection
