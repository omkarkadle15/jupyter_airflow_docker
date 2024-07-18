FROM apache/airflow:2.6.1

USER root
RUN apt-get update && apt-get install -y postgresql-client

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER airflow

COPY requirements.txt /requirements.txt
RUN pip install --user -r /requirements.txt

ENTRYPOINT ["/entrypoint.sh"]