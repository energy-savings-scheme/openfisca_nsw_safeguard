FROM python:3.12-slim AS build

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Install system dependencies required for building certain Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    make \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN uv venv
RUN uv pip install --editable .[dev] --upgrade

FROM python:3.12-slim AS runtime

COPY --from=build /app/.venv/ /app/.venv/

RUN apt-get update && apt-get install -y --no-install-recommends \
    nano \
    git \
    make \
    && rm -rf /var/lib/apt/lists/*

# # Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN ln -sf /bin/bash /bin/sh

WORKDIR /app

COPY . .

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["bash", "-c", "openfisca serve --reload --country-package openfisca_nsw_safeguard --bind 0.0.0.0:8080"]
