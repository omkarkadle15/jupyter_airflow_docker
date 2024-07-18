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

git clone https://github.com/omkarkadle15/jupyter_airflow_docker

cd (project-directory)

Replace "project directory" with the actual directory where you cloned the project.

2. Start your Jupyter Notebook server:

jupyter notebook --no-browser

Note the token provided in the Jupyter server output.

3. Allow Jupyter to be accessed externally and listen to all IPs:

Execute this command on powershell: jupyter notebook --generate-config

You will get the path to a file, namely "jupyter_notebook_config.py". Open that file and add these two lines anywhere you wish:

c.NotebookApp.allow_origin = '*' #allow all origins

c.NotebookApp.ip = '0.0.0.0' # listen on all IPs

4. Update the `dags/run_notebook.py` file with your Jupyter server details:

- Update the `base_url` with your Jupyter server's address
- Replace the `token` value with the token from step 2

5. Build the Docker images:

docker-compose build

6. Start the Airflow services:

docker-compose up

7. Access the Airflow web interface at `http://localhost:8080`

## Accessing Airflow

After starting the services, you can access the Airflow web interface at `http://localhost:8080`

Default login credentials:
- Username: admin
- Password: admin

**Note:** For security reasons, it's recommended to change these default credentials immediately after your first login in a production environment.

## Configuration

- The Airflow webserver is accessible on port 8080.
- Postgres is used as the database backend.
- The `run_notebook.py` DAG is configured to execute a notebook on a remote Jupyter server.

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

If you encounter any issues:

1. Ensure all required ports are available.
2. Check Docker and Docker Compose are installed and up to date.
3. Verify network connectivity to the remote Jupyter server.
4. If you're unable to log in, try resetting the database:
docker-compose down -v
docker-compose up
5. If the DAG fails to execute the notebook, check the Jupyter server token in `run_notebook.py`.

## Notes

- The entrypoint script (`entrypoint.sh`) handles service startup.
- The project is configured to use LocalExecutor for task execution.
- Database initialization is handled by the `airflow-init` service in `docker-compose.yaml`.
- Ensure your Jupyter Notebook server is running and accessible from the Docker network.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

## License

[Specify your license here]