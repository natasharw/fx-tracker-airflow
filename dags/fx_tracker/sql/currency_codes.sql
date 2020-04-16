COPY alphavantage.currency_codes
FROM '/usr/local/airflow/dags/fx_tracker/currency_codes.csv'
DELIMITER ',' CSV HEADER