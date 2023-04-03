-- Dataset Creation via Terraform:
-- Create the dataset `raw` using terraform with us-central1 as the zone

------------------------------------------------------------------------------------------------------------------------------------------------
-- TABLE CREATION TEST
-- EXTERNAL TABLE CREATIONS
-- Creating external table referring to the .parquet files that in the folder of the partitioned data (NOTE: you need to ignore the .crc files)
CREATE OR REPLACE EXTERNAL TABLE `blissful-flames-375219.sf_eviction.external_eviction`
OPTIONS (
  format = 'parquet',
  uris = ['gs://dtc_data_lake_blissful-flames-375219/data_eviction/2023/3/26/clean_partitioned_eviction_2023-03-26/*.parquet']
);

-- PARTITIONED TABLE CREATION
-- Create parititioned table from external table
CREATE OR REPLACE TABLE `blissful-flames-375219.sf_eviction.eviction_test`
PARTITION BY file_date
AS
SELECT * FROM `blissful-flames-375219.sf_eviction.external_eviction`;
-- ERROR: Too many partitions produced by query, allowed 4000, query produces at least 6389 partitions

-- Create partions on updated_at column and cluster by eviction_id
CREATE OR REPLACE TABLE `blissful-flames-375219.sf_eviction.eviction_partition`
PARTITION BY
DATE(updated_at)  
CLUSTER BY 
  eviction_id AS
SELECT * FROM `blissful-flames-375219.sf_eviction.external_eviction`
;

----------------------------------------------------------------------------------------------------------------------------------------------------
-- TEST QUERIES
--SELECT COUNT(*) FROM `blissful-flames-375219.sf_eviction.external_eviction`;

--SELECT DISTINCT(state) FROM `blissful-flames-375219.sf_eviction.external_eviction`;

--SELECT DISTINCT(city) FROM `blissful-flames-375219.sf_eviction.external_eviction`;

-- SELECT Candidates for partitioning
SELECT COUNT(DISTINCT(zip)) FROM `blissful-flames-375219.sf_eviction.external_eviction`;

SELECT zip, COUNT(1) FROM `blissful-flames-375219.sf_eviction.external_eviction`
GROUP BY zip;

SELECT COUNT(DISTINCT(file_date)) FROM `blissful-flames-375219.sf_eviction.external_eviction`;

SELECT file_date, COUNT(1) FROM `blissful-flames-375219.sf_eviction.external_eviction`
GROUP BY file_date;

SELECT DATE(created_at), COUNT(1)
FROM `blissful-flames-375219.staging.stg_eviction` 
GROUP BY 1
ORDER BY 1
;



