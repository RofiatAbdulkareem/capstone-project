{{ config(materialized='table') }}

SELECT
    country_id,
    country_name,
    currency_code,
    currency_symbol
FROM {{ ref('transformed_data_model') }}