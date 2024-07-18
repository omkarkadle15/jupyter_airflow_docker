#!/bin/bash
set -e

# Add user-installed packages to Python path
export PATH="/home/airflow/.local/bin:$PATH"

# Wait for PostgreSQL to be ready
while ! nc -z postgres 5432; do
    echo "Waiting for PostgreSQL to start..."
    sleep 2
done

# Execute the provided command (webserver or scheduler)
exec airflow "$@"