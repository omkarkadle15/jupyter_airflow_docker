FROM apache/airflow:2.6.1

USER root
RUN apt-get update && apt-get install -y postgresql-client
USER airflow

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt