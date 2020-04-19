SELECT
    date,
    from_currency,
    to_currency,
    (data->'open') AS open,
    (data->'high') AS high,
    (data->'low') AS low,
    (data->'close') AS close,
FROM alphavantage.daily_exchange_rates_pre_staging
