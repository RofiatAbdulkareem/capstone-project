{{ config(materialized='table') }}

SELECT
    country_id,
    population,
    area,
    population_density,
    ARRAY_LENGTH(string_to_array(languages, ',')::TEXT[], 1) AS languages_count,
    ARRAY_LENGTH(string_to_array(currency_code, ',')::TEXT[], 1) AS currencies_count
FROM {{ ref('transformed_data_model') }}