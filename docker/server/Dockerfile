FROM python:3.12-slim

RUN apt-get update && apt-get install --yes --no-install-recommends g++ libssl-dev && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install uv

WORKDIR /app

COPY ./docker/server/entrypoint.sh /entrypoint.sh

COPY ./server/pyproject.toml ./server/uv.lock ./

RUN uv sync

COPY ./server ./

RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]