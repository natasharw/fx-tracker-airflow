# FX Tracker

**** Work in progress ****

A dockerised pipeline to process exchange rate data using Airflow

## Prerequisites
* Docker
  * Check if installed by running `docker --version` on the command line
  * Can be installed from the [Docker website](https://docs.docker.com/install/)
* Python 3

## How to run

#### 1. Clone respository

```
git clone https://github.com/natasharw/fx-tracker-airflow.git
```

#### 2. Build the services
```
docker-compose build
```

#### 3. FIRST RUN ONLY: Initalize database
```
docker-compose up postgres
```
```
docker-compose initdb
```
#### 4. Run other services
On first run:
```
docker-compose up webserver scheduler worker redis flower
```
On future runs:
```
docker-compose up
```
