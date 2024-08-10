#!/bin/bash

# Create env files if they don't exist. Needs to run before the compose creates containers
if [ ! -f ./client/.env ]; then
    cp ./client/.env.example ./client/.env
fi
if [ ! -f ./server/.env ]; then
    cp ./server/.env.example ./server/.env
fi