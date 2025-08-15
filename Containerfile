FROM python:3.10-slim

ENV PIP_DEFAULT_TIMEOUT=100 \
    # Allow statements and log messages to immediately appear
    PYTHONUNBUFFERED=1 \
    # disable a pip version check to reduce run-time & log-spam
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    # cache is useless in docker image, so disable to reduce image size
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.6.1

WORKDIR /app

# Upgrade the package index and install security upgrades
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
    cron \
    # Clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

COPY ./pyproject.toml /app/
COPY ./README.md /app/
COPY ./ilo4/ /app/ilo4/
COPY ./run.py /app/

RUN pip install -e .

RUN chmod +x /app/run.py

# Add the cron job
RUN crontab -l | { cat; echo "5 * * * * cd /app/ && ./run.py"; } | crontab -

