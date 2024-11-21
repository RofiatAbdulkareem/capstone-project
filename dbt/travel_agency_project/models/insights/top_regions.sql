WITH region_data AS (
    SELECT
        dc.region,
        fc.population,
        fc.area
    FROM {{ ref('fact_country') }} fc
    JOIN {{ ref('dim_country') }} dc
    ON fc.country_id = dc.country_id 
)
SELECT
    region,
    SUM(population) AS total_population,
    SUM(area) AS total_area
FROM region_data
GROUP BY region
ORDER BY total_population DESC
