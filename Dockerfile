FROM python:3.12-slim

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY pyproject.toml ./

RUN uv venv

RUN uv pip install -r pyproject.toml

COPY . .

WORKDIR /app/src