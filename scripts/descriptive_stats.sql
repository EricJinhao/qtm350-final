SELECT country_code,
       indicator_code,
       MIN(value) AS min_val,
       MAX(value) AS max_val,
       AVG(value) AS avg_val
FROM wdi_values
GROUP BY country_code, indicator_code;
