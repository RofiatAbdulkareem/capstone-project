{{ config(materialized='table') }}

SELECT
    country_id,
    country_name,
    official_name,
    region,
    sub_region,
    independence,
    un_member,
    start_of_week
FROM {{ ref('transformed_data_model') }}