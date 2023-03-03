# multi-stage dockerfile
# By using a multi-stage Dockerfile, you can take advantage of the layer caching mechanism of Docker to reuse the dependencies and packages installed in the earlier stages. The final stage can access those dependencies and use them to build your application without having to install them again. This can significantly reduce the size of your Docker image and the build time.
ARG BUILD_STAGE_PYTHON_VERSION=3.9.13
ARG POETRY_VERSION=1.1.12
ARG AIRFLOW_VERSION=2.5.1-python3.9
ARG POETRY_HOME=/opt/poetry
ARG PROJECT_PATH=/project/dev



# BASE STAGE
FROM python:$BUILD_STAGE_PYTHON_VERSION as base_image

ARG POETRY_VERSION
ARG BUILD_STAGE_PYTHON_VERSION
ARG POETRY_HOME
ARG PROJECT_PATH

# configure settings and create variables for poetry
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

ENV POETRY_VERSION=$POETRY_VERSION \
    POETRY_HOME=$POETRY_HOME \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# Update essential packages
RUN apt-get update -y && apt-get install build-essential -y

# curl poetry repo and install it
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python3
ENV PATH="$POETRY_HOME/bin:$PATH"

# copy files so i can use requirements
COPY . ./$PROJECT_PATH



# BUILD STAGE
FROM base_image as build

ARG PROJECT_PATH

WORKDIR $PROJECT_PATH

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes



# FINAL STAGE
FROM apache/airflow:$AIRFLOW_VERSION

ARG PROJECT_PATH

USER airflow

# Copy files from before image to use requirements.txt
COPY --from=build $PROJECT_PATH $PROJECT_PATH

WORKDIR $PROJECT_PATH

RUN pip install -r requirements.txt --no-cache-dir
