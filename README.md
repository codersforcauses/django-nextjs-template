# django-nextjs-template

Django + Nextjs Template: Standardised CFC Tech Stack

## Get started

0. Activate the dev container in VSCode
1. Start the db, server and client with `docker compose up`
2. Server is at `localhost:8000`, client at `localhost:3000`

## Server

### Create and run migrations

If the models are updated, be sure to create a migration:

```bash
docker container exec server python manage.py makemigrations # create a new migration OR
dxc server python manage.py makemigrations
```

### Get Intellisense

If you're in the dev container, this should be done already. You can run `poetry install` to get the latest dependencies.

## Other

### Editing Docker stuff

If you modify anything in the `docker` folder, you need to add the `--build` flag or Docker won't give you the latest changes.

### Custom env vars

Make a copy of `.env.example` named `.env` in the respective directory and edit the environment variables.
