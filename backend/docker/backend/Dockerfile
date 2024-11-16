FROM python:3.12.7-slim-bullseye as base

RUN pip install --no-cache-dir --upgrade pip && pip install poetry
WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-dev --no-interaction --no-ansi

FROM base as migrations

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-dev --no-interaction --no-ansi

COPY . .