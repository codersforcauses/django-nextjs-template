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

# Nuke and migrate db
(cd server && ./nuke.sh)
