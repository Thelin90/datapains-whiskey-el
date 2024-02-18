FROM python:3.11-slim

COPY src /app/src/
COPY tests /app/tests/
COPY .git /app/.git/
COPY ["run.py", ".pre-commit-config.yaml", "Makefile", "poetry.lock", "pyproject.toml", "README.md", "/app/"]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_VERSION 24.0
ENV POETRY_VERSION 1.7.1

RUN apt-get update && \
    apt-get -y install --no-install-recommends libc-bin=2.36-9+deb12u4 && \
    apt-get -y install --no-install-recommends libc6=2.36-9+deb12u4 && \
    apt-get -y install --no-install-recommends git=1:2.39.2-1.1 && \
    apt-get -y install --no-install-recommends make=4.3-4.1 && \
    apt-get -y install --no-install-recommends libgnutls30=3.7.9-2+deb12u2 && \
    rm -rf /var/lib/apt/lists/* && \
    python -m pip install --no-cache-dir pip==${PIP_VERSION} && \
    pip install --no-cache-dir poetry==${POETRY_VERSION} && \
    make --directory /app/ install-environment
