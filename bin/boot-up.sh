#!/bin/bash

# Runs every single time on boot up of the container
echo "Booting up the environments for you"

docker compose up -d

cd server && python manage.py migrate

