import pandas as pd
import boto3
from sqlalchemy import create_engine
import io


def write_to_warehouse():
    """
    Reads transformed data from an S3 bucket and writes it to a PostgreSQL database.
    """
    try:
        # Step 1: Set up AWS S3 and SSM clients
        print("Initializing AWS clients...")
        s3_client = boto3.client('s3')
        ssm_client = boto3.client('ssm', region_name='us-east-1')

        # Step 2: Define S3 bucket and file details
        bucket_name = 'cde-travel-data-lake'
        file_key = 'transform/countries_data_transformed.parquet'

        # Step 3: Retrieve RDS password from AWS SSM Parameter Store
        print("Retrieving RDS password from SSM...")
        parameter_name = 'travel-agency-warehousepassword'
        rds_password = ssm_client.get_parameter(Name=parameter_name, WithDecryption=True)['Parameter']['Value']

        # Step 4: Read the Parquet file from S3
        print(f"Fetching Parquet file from S3 bucket '{bucket_name}'...")
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        df_transformed = pd.read_parquet(io.BytesIO(response['Body'].read()))

        # Step 5: Ensure all string columns are WIN1252-compatible
        print("Ensuring string columns are WIN1252-compatible...")
        for col in df_transformed.select_dtypes(include=['object']).columns:
            df_transformed[col] = df_transformed[col].apply(
                lambda x: x.encode('latin1', errors='ignore').decode('latin1') if isinstance(x, str) else x
            )

        # Step 6: Database connection parameters
        db_user = 'rofee'
        db_host = 'terraform-20241113122124605100000001.cz4qw448wzk4.us-east-1.rds.amazonaws.com'
        db_port = '5432'
        db_name = 'travel_agency_dw'
        connection_string = f'postgresql+psycopg2://{db_user}:{rds_password}@{db_host}:{db_port}/{db_name}'

        # Step 7: Create the SQLAlchemy engine
        print("Creating database engine...")
        engine = create_engine(connection_string)

        # Step 8: Load the data into the PostgreSQL table
        table_name = 'transformed_data'
        print(f"Loading data into the '{table_name}' table...")
        df_transformed.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
        print(f"Data successfully loaded into the '{table_name}' table in PostgreSQL.")

    except boto3.exceptions.Boto3Error as e:
        print(f"An AWS error occurred: {e}")
        raise
    except pd.errors.PandasError as e:
        print(f"An error occurred while handling the DataFrame: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise
    finally:
        # Ensure the database connection is disposed of properly
        try:
            engine.dispose()
            print("Database connection closed.")
        except NameError:
            pass


# Run the function (optional for testing)
if __name__ == "__main__":
    write_to_warehouse()
    