# base image
FROM python:3.10 AS base

WORKDIR /app/env
# set env variables
ENV PYTHONUNBUFFERED=1 \
    # set pip to disable version check
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # Poetry config
    POETRY_VERSION=1.6.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_VIRTUALENVS_CREATE=true

# install poetry
RUN pip install --no-cache-dir poetry==${POETRY_VERSION}

# builder image
FROM base AS builder
COPY pyproject.toml ./
COPY poetry.lock ./

# install dependencies
RUN --mount=type=cache,target=/root/.cache \
    poetry install --no-root --only main

# production image
FROM base AS production

# expose port
EXPOSE 8000

# set timezone to UTC
ENV TZ=UTC

# set work directory
WORKDIR /app/ApplicationDistributionCenter

# copy code to work dir
COPY . /app/ApplicationDistributionCenter

# Copy Python environment and packages
ENV VIRTUAL_ENV=/app/env/.venv
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

# copy entrypoint.sh
COPY ./docker/entrypoint.sh /


# add execute permission to entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh && chmod +x /entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]