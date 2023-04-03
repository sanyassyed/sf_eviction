{{ config(materialized='table') }}
-- only selecting the latest updated version of all eviction id's
WITH ord_tab AS
(
   SELECT *,
   row_number() over(partition by eviction_id order by updated_at desc) as rn
   FROM {{ ref('stg_eviction') }}
)
SELECT *
FROM ord_tab
WHERE rn = 1

