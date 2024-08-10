#!/bin/bash

# Runs once after devcontainer is created

figlet "1-time Setup"
echo "Running one-time setup for you :)"

# Install dependencies
(cd server && POETRY_VIRTUALENVS_CREATE=false poetry install)
(cd client && npm install)

# Nuke and migrate db
(cd server && ./nuke.sh)

# Make the Django static folder to remove the annoying warning
(cd server && mkdir -p static)