# multi-stage dockerfile
# By using a multi-stage Dockerfile, you can take advantage of the layer caching mechanism of Docker to reuse the dependencies and packages installed in the earlier stages. The final stage can access those dependencies and use them to build your application without having to install them again. This can significantly reduce the size of your Docker image and the build time.

# Inspiration: https://bmaingret.github.io/blog/2021-11-15-Docker-and-Poetry
ARG PROJECT_NAME=core
ARG PROJECT_PATH=/fac/$PROJECT_NAME
ARG POETRY_VERSION=1.3.2
ARG BUILD_PYTHON_VERSION=3.9.13
ARG AIRFLOW_VERSION=2.5.1-python3.9

# Base image to install poetry and copy files
FROM python:$BUILD_PYTHON_VERSION as base
ARG PROJECT_NAME
ARG PROJECT_PATH
ARG POETRY_VERSION
ARG PYTHON_VERSION

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

ENV POETRY_VERSION=$POETRY_VERSION \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python3
ENV PATH="$POETRY_HOME/bin:$PATH"

COPY . ./$PROJECT_PATH

# Build stage to export requirements and build the module
FROM base as build
ARG PROJECT_PATH

WORKDIR $PROJECT_PATH

RUN ls -la
RUN poetry build --format wheel

# Final stage that install the module and its requirements
FROM apache/airflow:$AIRFLOW_VERSION
ARG PROJECT_NAME
ARG PROJECT_PATH
ARG DBT_TYPE=$DBT_TYPE

USER airflow

COPY --from=build $PROJECT_PATH/dist/*.whl /tmp/dist/
RUN pip install --find-link /tmp/dist $PROJECT_NAME --user
