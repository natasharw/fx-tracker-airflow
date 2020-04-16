CREATE TABLE alphavantage.daily_exchange_rates_staging (
    date DATE,
    from_currency VARCHAR(3),
    to_currency VARCHAR(3),
    open REAL,
    high REAL,
    low REAL,
    close REAL
)
