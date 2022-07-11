FROM python:3.10-slim-buster AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

FROM base AS builder

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  && apt-get install -y python3-dev \
  && apt-get install -y curl \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Requirements are installed here to ensure they will be cached.
COPY requirements.txt requirements-dev.txt /

RUN pip install --prefix='/install' -r /requirements-dev.txt

FROM base

COPY --from=builder /install /usr/local

# Set user and group
RUN groupadd -g 1000 appuser
RUN useradd -u 1000 -g appuser -s /bin/sh -m appuser # <--- the '-m' create a user home directory

# Switch to user
USER 1000:1000

COPY . /app

WORKDIR /app
