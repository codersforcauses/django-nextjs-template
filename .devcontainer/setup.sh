#!/bin/bash

# Runs once after devcontainer is created

figlet "1-time Setup"
echo "Running one-time setup for you :)"

# We can set up in global because this only applies to the entire devcontainer
git config --global --add safe.directory /workspaces/* || true
git config --global --add safe.directory /workspace/* || true
git config --global --add --bool push.autoSetupRemote true

# Create .env files if it doesn't exist
if [ ! -f ./client/.env ]; then
    cp ./client/.env.example ./client/.env
fi
if [ ! -f ./server/.env ]; then
    cp ./server/.env.example ./server/.env
fi

# Make the Django static folder to remove the annoying warning
(cd server && mkdir -p static)

# Install dependencies
(cd server && POETRY_VIRTUALENVS_CREATE=false poetry install)
(cd client && npm install)

# Run the database in the background
docker compose up -d

# Wait for the database to start
# Get the container ID of the db service
DB_CONTAINER_ID=$(docker compose ps -q db)
echo "Waiting for the database to be ready..."
until [ "$(docker inspect -f '{{.State.Health.Status}}' "$DB_CONTAINER_ID")" == "healthy" ]; do
    sleep 1
done

# Nuke and migrate db
(cd server && ./nuke.sh)
