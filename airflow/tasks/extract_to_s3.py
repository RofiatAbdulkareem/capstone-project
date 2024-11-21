"""
A script to fetch country data from an API, save it as a Parquet file,
and upload it to an S3 bucket.
"""

import os
import requests
import pandas as pd
import boto3

# Constants for API and S3
API_ENDPOINT = "https://restcountries.com/v3.1/all"
S3_BUCKET_NAME = "cde-travel-data-lake"
S3_FILE_NAME = "raw_data/countries.parquet"


def extract_data():
    try:
        # Step 1: Fetch data from API
        print("Fetching data from API...")
        response = requests.get(API_ENDPOINT, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Step 2: Convert data to a DataFrame
        print("Converting data to DataFrame...")
        df = pd.DataFrame(data)

        # Step 3: Save data as a Parquet file locally
        print("Saving data to Parquet file...")
        local_file_path = "countries.parquet"
        df.to_parquet(local_file_path, engine="pyarrow", index=False)

        # Step 4: Upload Parquet file to S3
        print("Uploading Parquet file to S3...")
        s3_client = boto3.client("s3")
        with open(local_file_path, "rb") as file:
            s3_client.upload_fileobj(file, S3_BUCKET_NAME, S3_FILE_NAME)
        print(f"uploaded to: {S3_FILE_NAME}")

        # Step 5: Clean up local file
        os.remove(local_file_path)
        print("Cleaned up local file.")

    except requests.exceptions.RequestException as api_error:
        print(f"Failed to fetch data from API: {api_error}")
        raise
    except boto3.exceptions.Boto3Error as s3_error:
        print(f"Failed to upload data to S3: {s3_error}")
        raise
    except Exception as general_error:
        print(f"An unexpected error occurred: {general_error}")
        raise


if __name__ == "__main__":
    extract_data()
