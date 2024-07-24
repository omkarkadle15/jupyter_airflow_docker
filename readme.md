# Airflow Docker Project with Remote Jupyter Notebook Execution

This project sets up an Apache Airflow environment using Docker, configured to execute Jupyter notebooks located on a remote server.

## Project Structure

- `docker-compose.yaml`: Defines the services (Postgres, Airflow webserver, scheduler, and initialization).
- `Dockerfile`: Custom Airflow image with additional dependencies.
- `entrypoint.sh`: Script to start Airflow services.
- `requirements.txt`: Additional Python packages required for the project.
- `dags/run_notebook.py`: Airflow DAG to execute remote Jupyter notebooks.

## Prerequisites

- Docker
- Docker Compose
- Jupyter Notebook server (running separately)

## Setup and Running

1. Clone this repository:

git clone https://github.com/omkarkadle15/jupyter_airflow_docker.git
cd (the directory where you cloned this project)

2. Start your Jupyter Notebook server:

jupyter notebook --no-browser

Note the token provided in the Jupyter server output.

3. Configure Jupyter to allow external access:
- Generate a config file if you don't have one:
  ```
  jupyter notebook --generate-config
  ```
- Edit the `jupyter_notebook_config.py` file and add:
  ```python
  c.NotebookApp.allow_origin = '*'
  c.NotebookApp.ip = '0.0.0.0'
  ```

4. Build the Docker images:

docker-compose build

5. Start the airflow services:

docker-compose up

6. Access the Airflow web interface at `http://localhost:8080`

## Accessing Airflow

- URL: `http://localhost:8080`
- Default login credentials:
- Username: admin
- Password: admin

**Note:** Change these default credentials immediately after your first login in a production environment.

## Configuring Jupyter Notebook Settings

You can change the Jupyter Notebook settings directly from the Airflow UI without rebuilding Docker containers:

1. Go to Admin -> Variables in the Airflow UI.
2. Add or update the following variables:
- `base_url`: The URL of your Jupyter Notebook server
- `notebook_path`: The path to the notebook you want to execute
- `token`: Your Jupyter Notebook server token

This allows you to easily modify the Jupyter Notebook configuration without redeploying the entire setup.

## Configuration

- Airflow webserver is accessible on port 8080.
- Postgres is used as the database backend.
- The `run_notebook.py` DAG executes a notebook on a remote Jupyter server.

## Customization

- Modify `run_notebook.py` to change the remote Jupyter server details or the notebook to be executed.
- Add additional DAGs in the `dags/` directory.
- Modify `requirements.txt` to add or remove Python dependencies.

## Services

1. **postgres**: PostgreSQL database for Airflow metadata.
2. **airflow-init**: Initializes the Airflow database and creates the admin user.
3. **webserver**: Runs the Airflow web server.
4. **scheduler**: Runs the Airflow scheduler.

## Troubleshooting

If you encounter issues:

1. Ensure all required ports are available.
2. Check Docker and Docker Compose are installed and up to date.
3. Verify network connectivity to the remote Jupyter server.
4. If unable to log in, try resetting the database:

docker-compose down -v
docker-compose up

5. If the DAG fails to execute the notebook, check the Jupyter server token in Airflow variables.

## Notes

- The entrypoint script (`entrypoint.sh`) handles service startup.
- The project uses LocalExecutor for task execution.
- Database initialization is handled by the `airflow-init` service.
- Ensure your Jupyter Notebook server is running and accessible from the Docker network.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

## License

[Specify your license here]