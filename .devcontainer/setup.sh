#!/bin/bash

# Runs once after devcontainer is created

figlet "1-time Setup"
echo "Running one-time setup for you :)"

# Create .env files if it doesn't exist
if [ ! -f ./client/.env ]; then
    cp ./client/.env.example ./client/.env
fi
if [ ! -f ./server/.env ]; then
    cp ./server/.env.example ./server/.env
fi

# Install dependencies
(cd server && POETRY_VIRTUALENVS_CREATE=false poetry install)
(cd client && npm install)

# Nuke and migrate db
(cd server &&
python manage.py reset_db --noinput
python manage.py migrate --noinput &&
python manage.py createsuperuser --noinput)

# Make the Django static folder to remove the annoying warning
(cd server && mkdir -p static)