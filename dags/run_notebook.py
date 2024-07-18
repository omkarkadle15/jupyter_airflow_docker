from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import papermill as pm
import requests
import json
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

def execute_remote_notebook(**kwargs):
    base_url = "http://host.docker.internal:8888"
    notebook_path = "Notebooks/notebook.ipynb"
    token = "b664613cce40a5ec23143c153c015ad942e6b779e36c55e2"
    headers = {"Authorization": f"Token {token}"}

    try:
        # Get the notebook content
        response = requests.get(f"{base_url}/api/contents/{notebook_path}", headers=headers)
        response.raise_for_status()
        notebook_content = response.json()

        # Load the notebook
        nb = nbformat.reads(json.dumps(notebook_content['content']), as_version=4)

        # Execute the notebook
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
        ep.preprocess(nb, {'metadata': {'path': '/tmp/'}})

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

        print(f"Notebook executed and updated successfully on the server.")

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to notebook: {str(e)}")
        raise AirflowException(f"Failed to connect to Jupyter notebook: {str(e)}")
    except Exception as e:
        print(f"Error processing notebook: {str(e)}")
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
    schedule_interval=timedelta(days=1),
)

run_notebook = PythonOperator(
    task_id='run_notebook',
    python_callable=execute_remote_notebook,
    dag=dag,
)

run_notebook