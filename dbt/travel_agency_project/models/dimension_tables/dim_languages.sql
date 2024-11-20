{{ config(materialized='table') }}

SELECT
    country_id,
    languages
FROM {{ ref('transformed_data_model') }}