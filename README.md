# django-nextjs-template

Django + Nextjs Template: Standardised CFC Tech Stack

## Get started

0. Activate the dev container in VSCode
1. Create a copy of `.env.example` found in the `client` folder and name it `.env`
2. Create a copy of `.env.example` found in the `server` folder and name it `.env`
3. Start the db, server and client with `docker compose up`
4. Server is at `localhost:8000`, client at `localhost:3000`

## Server

### Create and run migrations

If the models are updated, be sure to create a migration:

```bash
docker container exec server python manage.py makemigrations # create a new migration
docker container exec python manage.py migrate # apply migrations
```
