FROM python:3.12-slim AS build

# Install system dependencies required for building certain Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    nano \
    git \
    make \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

# RUN uv venv
RUN pip install --editable .[dev] --upgrade

# prioritize this gunicorn version to have compatibility with python 3.12
RUN pip install gunicorn~=21.0

FROM python:3.12-slim AS runtime

COPY --from=build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=build /usr/local/bin /usr/local/bin
COPY --from=build /usr/bin /usr/bin

# # Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN ln -sf /bin/bash /bin/sh

WORKDIR /app

COPY . .

CMD ["bash", "-c", "openfisca serve --reload --country-package openfisca_nsw_safeguard --bind 0.0.0.0:8080"]
