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
    (cd client && npm install &)
fi
(cd server && poetry install &)
docker compose pull &

# Wait for the installation to finish
wait

docker compose up -d

source ./server/.env
cd server && python manage.py migrate

