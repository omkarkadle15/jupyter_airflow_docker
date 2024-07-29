from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import papermill as pm
import requests
import json
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from airflow.exceptions import AirflowException
import logging
import os
from airflow.models import Variable

base_url = Variable.get("base_url", "http://host.docker.internal:8888")
notebook_path = Variable.get("notebook_path", "default-notebook.ipynb") # Make sure to change the default notebook
token = Variable.get("token")

def execute_remote_notebook(**kwargs):
    headers = {"Authorization": f"Token {token}"}

    try:
        # Get the notebook content
        response = requests.get(f"{base_url}/api/contents/{notebook_path}", headers=headers)
        response.raise_for_status()
        notebook_content = response.json()

        # Load the notebook
        nb = nbformat.reads(json.dumps(notebook_content['content']), as_version=4)

        # Add environment variables to notebook metadata
        nb.metadata.papermill = {
            'INPUT_DIR': os.environ.get('INPUT_DIR', '/opt/airflow/input'),
            'OUTPUT_DIR': os.environ.get('OUTPUT_DIR', '/opt/airflow/output')
        }

        # Execute the notebook
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
        ep.preprocess(nb, {'metadata': {'path': '/tmp/'}})

        # Log the outputs
        for cell in nb.cells:
            if cell.cell_type == 'code':
                logging.info(f"Code:\n{cell.source}")
                if 'outputs' in cell:
                    for output in cell.outputs:
                        if output.output_type == 'stream':
                            logging.info(f"Output:\n{output.text}")
                        elif output.output_type == 'execute_result':
                            logging.info(f"Output:\n{output.data.get('text/plain', '')}")

        # Prepare the updated notebook content
        updated_content = {
            "type": "notebook",
            "content": json.loads(nbformat.writes(nb)),
            "format": "json"
        }

        # Save the executed notebook back to the server
        response = requests.put(
            f"{base_url}/api/contents/{notebook_path}",
            headers=headers,
            json=updated_content
        )
        response.raise_for_status()

        logging.info("Notebook executed and updated successfully on the server.")

    except requests.exceptions.RequestException as e:
        logging.error(f"Error connecting to notebook: {str(e)}")
        raise AirflowException(f"Failed to connect to Jupyter notebook: {str(e)}")
    except Exception as e:
        logging.error(f"Error processing notebook: {str(e)}")
        raise AirflowException(f"Failed to process Jupyter notebook: {str(e)}")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'run_remote_jupyter_notebook',
    default_args=default_args,
    description='A DAG to run a remote Jupyter notebook',
    schedule_interval=None,
    max_active_tasks=1,
    max_active_runs=1
)

run_notebook = PythonOperator(
    task_id='run_notebook',
    python_callable=execute_remote_notebook,
    dag=dag
)

run_notebook