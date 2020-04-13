FROM puckel/docker-airflow:1.10.6

RUN pip install --user --upgrade pip
RUN pip install --user papermill psycopg2-binary

ENV AIRFLOW_HOME=/usr/local/airflow

COPY ./airflow.cfg /usr/local/airflow/airflow.cfg
