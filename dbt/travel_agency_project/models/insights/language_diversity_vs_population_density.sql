{{ config(materialized='view') }}

SELECT
    CORR(fc.languages_count, fc.population_density) AS correlation
FROM {{ ref('fact_country') }} fc