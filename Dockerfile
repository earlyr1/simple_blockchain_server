FROM python:3.10-alpine3.15 AS os

RUN apk add --no-cache \
        curl \
        gcc \
        libressl-dev \
        musl-dev \
        libffi-dev \
        bash

RUN pip install poetry
RUN poetry config virtualenvs.create false

FROM os AS build

COPY bc_server ./bc_server
COPY poetry.lock .
COPY pyproject.toml .
RUN poetry install --no-dev

FROM build AS production

RUN pip install uvicorn
EXPOSE 8080
CMD [ "uvicorn", "bc_server.main:app", "--host", "0.0.0.0", "--port", "8080" ]

FROM os as test

COPY bc_server ./bc_server
COPY tests ./tests
COPY pyproject.toml .
RUN poetry install
CMD [ "pytest", "./tests" ]