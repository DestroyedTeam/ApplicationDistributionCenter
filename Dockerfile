FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /ApplicationDistributionCenter

# Install dependencies
COPY ./pyproject.toml poetry.lock /ApplicationDistributionCenter/
RUN pip install poetry && poetry config virtualenvs.create false && poetry install

# Copy project
COPY . /ApplicationDistributionCenter/

# Expose port
EXPOSE 8000

COPY ./docker/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]