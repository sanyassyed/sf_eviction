{{config(materialized='view')}}
--handling deduplication
with evicdata as
(
select *,
row_number() over(partition by eviction_id, updated_at) as rn
from {{ source('staging', var("BQ_TABLE_NAME_EVICTION")) }}
)

select 
--here we are using the date_trunc function from dbt_utils
cast( ({{dbt_utils.surrogate_key(['eviction_id', date_trunc('day', 'updated_at')])}}) as string) as case_id,
--here we are using the date_truc function from BQ hence the syntax is different
--Not using this as I've alreasy eliminated duplicates of these by using de-duplication above
--concat(eviction_id, '_', DATE(updated_at)) as case_id,
cast(eviction_id as string) as eviction_id, 
cast(address as string) as address, 
cast(city as string) as city, 
cast(state as string) as state, 
cast(zip as integer) as zip, 
cast(file_date as date) as file_date, 
cast(non_payment as boolean) as non_payment, 
cast(breach as boolean) as breach, 
cast(nuisance as boolean) as nuisance, 
cast(illegal_use as boolean) as illegal_use, 
cast(failure_to_sign_renewal as boolean) as failure_to_sign_renewal, 
cast(access_denial as boolean) as access_denial, 
cast(unapproved_subtenant as boolean) as unapproved_subtenant, 
cast(owner_move_in as boolean) as owner_move_in, 
cast(demolition as boolean) as demolition, 
cast(capital_improvement as boolean) as capital_improvement, 
cast(substantial_rehab as boolean) as substantial_rehab, 
cast(ellis_act_withdrawal as boolean) as ellis_act_withdrawal, 
cast(condo_conversion as boolean) as condo_conversion, 
cast(roommate_same_unit as boolean) as roommate_same_unit, 
cast(other_cause as boolean) as other_cause, 
cast(late_payments as boolean) as late_payments, 
cast(lead_remediation as boolean) as lead_remediation, 
cast(development as boolean) as development, 
cast(good_samaritan_ends as boolean) as good_samaritan_ends, 
cast(constraints_date as timestamp) as constraints_date, 
cast(supervisor_district as integer) as supervisor_district, 
cast(neighborhood as string) as neighborhood, 
cast(created_at as timestamp) as created_at, 
cast(updated_at as timestamp) as updated_at, 
cast(longitude as FLOAT64) as longitude, 
cast(latitude as FLOAT64) as latitude,
--ST_GEOPOINT is a BQ function
cast(ST_GEOGPOINT(longitude, latitude) as geography) as location

from evicdata
where rn = 1

-- dbt build --m <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

    limit 100

{% endif %}


