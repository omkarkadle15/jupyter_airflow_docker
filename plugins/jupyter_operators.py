from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import requests
import json
import nbformat
from nbclient import NotebookClient

class JupyterExecuteOperator(BaseOperator):
    @apply_defaults
    def __init__(
        self,
        jupyter_url,
        notebook_path,
        jupyter_token,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.jupyter_url = jupyter_url
        self.notebook_path = notebook_path
        self.jupyter_token = jupyter_token

    def execute(self, context):
        headers = {"Authorization": f"Token {self.jupyter_token}"}
        notebook_url = f"{self.jupyter_url}/api/contents/{self.notebook_path}"

        # Get the notebook content
        response = requests.get(notebook_url, headers=headers)
        if response.status_code != 200:
            raise ValueError(f"Failed to get notebook: {response.status_code}")

        notebook_data = response.json()

        # Load the notebook
        nb = nbformat.reads(json.dumps(notebook_data['content']), as_version=4)

        # Execute the notebook
        client = NotebookClient(nb, timeout=600)
        executed_nb = client.execute()

        # Save the executed notebook back to the server
        payload = {
            "type": "notebook",
            "content": json.loads(nbformat.writes(executed_nb))
        }
        response = requests.put(notebook_url, headers=headers, json=payload)
        if response.status_code != 200:
            raise ValueError(f"Failed to save notebook: {response.status_code}")

        self.log.info("Notebook executed successfully")