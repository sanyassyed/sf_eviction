{{config(materialized='table')}}

select * from {{ source('staging', var("BQ_TABLE_NAME_EVICTION")) }}

{% if var('is_test_run', default=true) %}

    limit 100

{% endif %}