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

# if node_modules doesn't exist, install it
if [ ! -d ./client/node_modules ]; then
    (cd client && npm install)
fi
# TODO Figure out why this env variable is not getting loaded
# probably because it needs to be added in .zprofile
export POETRY_VIRTUALENVS_CREATE=false
(cd server && poetry install && poetry show -v)

docker compose pull

docker compose up -d

source ./server/.env
cd server && python manage.py migrate

