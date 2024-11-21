SELECT
    start_of_week,
    COUNT(*) AS country_count
FROM {{ ref('dim_country') }} 
GROUP BY start_of_week
ORDER BY country_count DESC
