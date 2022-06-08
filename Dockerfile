FROM python:3.10-slim-buster
ARG DB_USER
ARG DB_PASSWORD
ENV POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_NO_INTERACTION=1 \
    DB_USER=${DB_USER} \
    DB_PASSWORD=${DB_PASSWORD}
ENV PATH=${POETRY_HOME}/bin:${PATH}

RUN apt-get update && \
    apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /g4y0f7h3d4y

COPY pyproject.toml poetry.lock ./
COPY src src

RUN poetry install --no-dev
CMD poetry run gunicorn -b 0.0.0.0:${PORT} -k uvicorn.workers.UvicornWorker src.main:app
