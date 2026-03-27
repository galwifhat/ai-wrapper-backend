#!/bin/bash

# Change to project root (optional, if you run the script from anywhere)
cd "$(dirname "$0")"

# Activate Pipenv shell automatically
PIPENV=$(command -v pipenv)
if [ -z "$PIPENV" ]; then
    echo "Error: pipenv is not installed."
    exit 1
fi

# Kill any existing Gunicorn processes on port 8000 (avoid conflicts)
echo "Checking for existing Gunicorn processes on port 8000..."
PID=$(lsof -ti :8000)
if [ ! -z "$PID" ]; then
    echo "Killing existing process $PID..."
    kill -9 $PID
fi

# Start Gunicorn with Flask app
echo "Starting backend on port 8000..."
pipenv run gunicorn --reload -b 0.0.0.0:8000 run:app


# Activate the Pipenv environment automatically
# Kill any old Gunicorn processes on the same port
# Start Gunicorn on your chosen port with --reload for development
