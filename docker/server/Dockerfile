FROM astral/uv:0.9-python3.14-bookworm-slim

RUN apt-get update && apt-get upgrade --yes  && apt-get install --yes --no-install-recommends postgresql-client g++ libssl-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./docker/server/entrypoint.sh /entrypoint.sh

COPY ./server/pyproject.toml ./server/uv.lock ./

RUN uv sync --frozen

COPY ./server ./

RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]
