INSERT INTO alphavantage.daily_exchange_rates (
    der_date,
    der_from_currency,
    der_to_currency,
    der_open,
    der_high,
    der_low,
    der_close,
    der_created_at,
    der_updated_at,
    der_deleted_at)
SELECT
    date,
    from_currency,
    to_currency,
    open,
    high,
    low,
    close,
    NOW(),
    NOW(),
    NULL
FROM alphavantage.daily_exchange_rates_staging
LEFT JOIN alphavantage.daily_exchange_rates
ON date = der_date
AND from_currency = der_from_currency
AND to_currency = der_to_currency
WHERE der_date IS NULL
