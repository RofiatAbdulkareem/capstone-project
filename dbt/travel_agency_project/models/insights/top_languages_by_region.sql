{{ config(materialized='view') }}

SELECT
    c.region,
    l.languages,
    COUNT(*) AS language_count
FROM {{ ref('dim_country') }} c
JOIN {{ ref('dim_languages') }} l ON c.country_id = l.country_id
GROUP BY c.region, l.languages
ORDER BY language_count DESC