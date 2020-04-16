CREATE TABLE alphavantage.daily_exchange_rates (
    der_date DATE,
    der_from_currency VARCHAR(3),
    der_to_currency VARCHAR(3),
    der_open REAL,
    der_high REAL,
    der_low REAL,
    der_close REAL,
    der_created_at TIMESTAMP WITHOUT TIME ZONE,
    der_updated_at TIMESTAMP WITHOUT TIME ZONE,
    der_deleted_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL
)
