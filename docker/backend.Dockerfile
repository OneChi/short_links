FROM python:3.8

WORKDIR /code

RUN apt-get -y update && \
    apt-get -y install build-essential postgresql-client

COPY backend /code/backend
COPY bin /code/bin

WORKDIR /code/backend

RUN pip install --upgrade pip
RUN pip install poetry

COPY ./backend/poetry.lock ./backend/pyproject.toml ./
RUN poetry install
