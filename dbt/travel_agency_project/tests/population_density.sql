select *
from {{ ref('transformed_data_model') }}
where transformed_data_model.population_density < 0