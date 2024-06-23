# django-nextjs-template

Django + Nextjs Template: Standardised CFC Tech Stack

## Get started

0. Activate the dev container in VSCode
1. Create a copy of `.env.example` found in the `client` folder and name it `.env`
2. Create a copy of `.env.example` found in the `server` folder and name it `.env`
3. Start the db, server and client with `docker compose up`

## Server

### Create and run migrations

If the models are updated, be sure to create a migration:

```bash
python manage.py makemigrations # create a new migration
python manage.py migrate # apply migrations
```
