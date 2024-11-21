{{ config(materialized='view') }}

SELECT
    dc.continents AS continent,
    SUM(fc.currencies_count) AS total_currencies
FROM {{ ref('dim_country') }} dc
JOIN {{ ref('fact_country') }} fc 
    ON dc.country_id = fc.country_id
GROUP BY dc.continents
ORDER BY total_currencies DESC