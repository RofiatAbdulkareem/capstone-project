{{ config(materialized='view') }}

SELECT
    country_name,
    population_density,
    RANK() OVER (ORDER BY population_density DESC) AS rank_high_density,
    RANK() OVER (ORDER BY population_density ASC) AS rank_low_density
FROM {{ ref('fact_country') }}
