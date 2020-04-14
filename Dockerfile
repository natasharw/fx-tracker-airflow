FROM puckel/docker-airflow:1.10.6

RUN python -m pip install --user --upgrade pip
RUN python -m pip install --user jupyter psycopg2-binary
COPY requirements.txt /usr/local/airflow/
RUN python -m pip install --user -r requirements.txt

ENV AIRFLOW_HOME=/usr/local/airflow

COPY ./airflow.cfg /usr/local/airflow/airflow.cfg
