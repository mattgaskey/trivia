#!/bin/bash
set -e

# Wait for the database to be ready
echo "Waiting for database to start..."
while ! nc -z db 5432; do
  sleep 1
done

echo "Database started"

# Debug: Check the Python environment and installed packages
echo "Checking Python environment..."
poetry run python -c "import sys; print(sys.executable)"
poetry run python -m pip list

# Set the PostgreSQL password
export PGPASSWORD=postgres

# Check if the trivia database exists, and create it if it doesn't
echo "Checking if the trivia database exists..."
if ! poetry run psql -h db -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'trivia'" | grep -q 1; then
  echo "Database trivia does not exist. Creating..."
  poetry run createdb -h db -U postgres trivia
  echo "Populating the trivia database..."
  poetry run psql -h db -U postgres -d trivia -f trivia.psql
else
  echo "Database trivia already exists."
fi

# Start your Flask application
echo "Starting Flask application..."
exec poetry run flask run --host=0.0.0.0 --reload