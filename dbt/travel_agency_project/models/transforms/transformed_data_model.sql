with base as (
    select *
    from {{ source('travel_agency_project', 'transformed_data') }}
)

select
    ROW_NUMBER() OVER () AS country_id, --Assign unique id's to each row
    country_name,
    official_name,
    continents,
    region,
    sub_region,
    independence,
    un_member,
    start_of_week,
    population,
    area,
    population / nullif(area, 0) as population_density,
    currency_code,
    currency_name,
    currency_symbol,
    languages,
    idd_code,
    capital
from base