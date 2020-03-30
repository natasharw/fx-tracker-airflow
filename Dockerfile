FROM puckel/docker-airflow:1.10.6
RUN pip install --user psycopg2-binary
ENV AIRFLOW_HOME=/user/local/airflow
# COPY /airflow.cfg /usr/local/airflow/airflow.cfg