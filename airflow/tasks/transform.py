import boto3
import pandas as pd
import io
import requests

# AWS S3 configuration
S3_BUCKET_NAME = 'cde-travel-data-lake'
S3_TRANSFORMED_KEY = 'transform/countries_data_transformed.parquet'

# API endpoint
API_ENDPOINT = "https://restcountries.com/v3.1/all"

def safe_get(dictionary, *keys):
    """
    Safely navigate nested dictionaries and lists.
    Returns None if any level of nesting is None or the key is missing.
    """
    result = dictionary
    for key in keys:
        if isinstance(result, dict):
            result = result.get(key)
        else:
            return None
    return result

def extract_currency_info(currency_dict):
    if isinstance(currency_dict, dict):
        for code, details in currency_dict.items():
            return {
                'currency_code': code,
                'currency_name': safe_get(details, 'name'),
                'currency_symbol': safe_get(details, 'symbol')
            }
    return {'currency_code': None, 'currency_name': None, 'currency_symbol': None}

def transform_data():
    try:
        # Fetch data from API
        response = requests.get(API_ENDPOINT)
        response.raise_for_status()
        data = response.json()

        # Extract relevant data with safe handling
        extracted_data = []
        for country in data:
            country_info = {
                'country_name': safe_get(country, 'name', 'common'),
                'official_name': safe_get(country, 'name', 'official'),
                'independence': country.get('independent', None),
                'un_member': country.get('unMember', None),
                'start_of_week': country.get('startOfWeek', None),
                'idd_code': f"{safe_get(country, 'idd', 'root') or ''}{''.join(safe_get(country, 'idd', 'suffixes') or [])}",
                'capital': (safe_get(country, 'capital') or [None])[0],
                'region': country.get('region', None),
                'sub_region': country.get('subregion', None),
                'languages': ', '.join((safe_get(country, 'languages') or {}).values()),
                'area': country.get('area', None),
                'population': country.get('population', None),
                'continents': ', '.join(safe_get(country, 'continents') or [])
            }

            # Extract currency information
            currency_info = extract_currency_info(country.get('currencies'))
            country_info.update(currency_info)

            extracted_data.append(country_info)

        # Create a DataFrame from the transformed data
        df_transformed = pd.DataFrame(extracted_data)

        # Save the transformed DataFrame as a Parquet file in S3
        s3_client = boto3.client('s3')
        parquet_buffer = io.BytesIO()
        df_transformed.to_parquet(parquet_buffer, index=False)

        s3_client.put_object(Bucket=S3_BUCKET_NAME, Key=S3_TRANSFORMED_KEY, Body=parquet_buffer.getvalue())
        print("Transformed data saved successfully to S3.")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data from API: {e}")
        raise
    except boto3.exceptions.Boto3Error as e:
        print(f"Failed to save data to S3: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise
