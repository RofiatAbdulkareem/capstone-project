import requests
import pandas as pd
import boto3
import os


API_ENDPOINT = "https://restcountries.com/v3.1/all"
S3_BUCKET_NAME = "cde-travel-data-lake"
S3_FILE_NAME = "raw_data/countries.parquet"

def extract_data():
    try:
        # Fetch data from the API
        response = requests.get(API_ENDPOINT)
        response.raise_for_status()
        data = response.json()

        # Convert JSON data to a DataFrame
        df = pd.DataFrame(data)

        # Save DataFrame as a Parquet file
        local_file_path = "countries.parquet"
        df.to_parquet(local_file_path, engine="pyarrow", index=False)

        # Upload the Parquet file to S3
        s3_client = boto3.client('s3')
        with open(local_file_path, "rb") as f:
            s3_client.upload_fileobj(f, S3_BUCKET_NAME, S3_FILE_NAME)

        print(f"Data successfully extracted and saved to S3 as Parquet: {S3_FILE_NAME}")

        # Clean up local file
        os.remove(local_file_path)

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data from API: {e}")
        raise
    except boto3.exceptions.Boto3Error as e:
        print(f"Failed to upload data to S3: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise
