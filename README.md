# FX Tracker

A pipeline to process exchange rate data built with Airflow, Postgres, Docker and Jupyter.

## Overview
<b>Project is WIP</b>

This is a sandbox project to set up an environment with Airflow and Docker in order to schedule and monitor pipelines.

To demonstrate the environment, it is used to fetch daily exchange rate data from an external API (Alpha Vantage), load into a Postgres database, transform the raw data into reporting tables, and refresh a (currently dummy) Jupyter notebook.

<b>Notable features are:</b>
* `docker-compose` to launch Postgres instance and `LocalExecutor` Airflow setup
   * Airflow tasks run on same machine as scheduler
   * Parallelisation of tasks possible
* Alpha Vantage custom plugin
  * Custom hook to Alpha Vantage API
  * Custom operator to load data from Alpha Vantage to Postgres <b>(WIP)</b>
* `PapermillOperator` used to refresh Jupyter notebook

## Prerequisites
* Docker

## Setup

#### Clone respository
```
git clone https://github.com/natasharw/fx-tracker-airflow.git
```

#### Move into new directory
```
cd fx-tracker-airflow
```

#### Generate a fernet key for your environment and pipe into env file
```
echo $(echo "FERNET_KEY='")$(openssl rand -base64 32)$(echo "'") >> airflow.env
```
#### Sign up for free API key from Alphavantage
* Open browser to `https://www.alphavantage.co/support/#api-key` and follow instructions


#### Set up Airflow connection in env file for your new API key
```
echo 'AIRFLOW__CORE__ALPHAVANTAGE_CONN_ID=http://:@https://www.alphavantage.co/query:/?apikey=YOUR_KEY_HERE' >> airflow.env
```
#### Launch docker containers in detached session
```
docker-compose up --build -d
```

#### Initialise database for webserver (first time only)
```
docker-compose exec webserver airflow initdb
```



## Trigger pipeline
#### Trigger from command line
```
docker-compose exec webserver airflow trigger_dag daily_exchange_rates
```
#### Or trigger from web UI
* Open browser to `http://127.0.0.1:8080/`


## End
#### Close docker session
```
docker-compose down
```