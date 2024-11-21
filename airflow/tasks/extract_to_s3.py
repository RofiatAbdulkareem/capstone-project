import requests
import pandas as pd
import boto3
import os


# Constants
API_ENDPOINT = "https://restcountries.com/v3.1/all"
S3_BUCKET_NAME = "cde-travel-data-lake"
S3_FILE_NAME = "raw_data/countries.parquet"


def extract_data():
    """
    Extract data from the RestCountries API and save it to an S3 bucket as a Parquet file.
    """
    try:
        # Step 1: Fetch data from the API
        print("Fetching data from the API...")
        response = requests.get(API_ENDPOINT)
        response.raise_for_status()  # Raise an error for HTTP issues
        data = response.json()

        # Step 2: Convert JSON data to a DataFrame
        print("Converting data to DataFrame...")
        df = pd.json_normalize(data)  # Flatten nested JSON data into a table

        # Step 3: Save the DataFrame locally as a Parquet file
        local_file_path = "countries.parquet"
        print(f"Saving data locally as {local_file_path}...")
        df.to_parquet(local_file_path, engine="pyarrow", index=False)

        # Step 4: Upload the Parquet file to S3
        print(f"Uploading {local_file_path} to S3 bucket '{S3_BUCKET_NAME}'...")
        s3_client = boto3.client('s3')
        with open(local_file_path, "rb") as f:
            s3_client.upload_fileobj(f, S3_BUCKET_NAME, S3_FILE_NAME)
        print(f"Data successfully uploaded to S3 as {S3_FILE_NAME}.")

        # Step 5: Clean up the local file
        os.remove(local_file_path)
        print("Local file removed.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from the API: {e}")
        raise
    except boto3.exceptions.Boto3Error as e:
        print(f"Error uploading data to S3: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise


# Run the extract function (optional)
if __name__ == "__main__":
    extract_data()
