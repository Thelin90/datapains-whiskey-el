FROM python:3.10-slim-bullseye

COPY src /app/src/
COPY tests /app/tests/
COPY .git /app/.git/
COPY ["run.py", ".pre-commit-config.yaml", "Makefile", "poetry.lock", "pyproject.toml", "README.md", "/app/"]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_VERSION 24.0
ENV POETRY_VERSION 1.7.1

RUN apt-get update && \
    apt-get -y install --no-install-recommends libc-bin=2.31-13+deb11u8 && \
    apt-get -y install --no-install-recommends libc6=2.31-13+deb11u8 && \
    apt-get -y install --no-install-recommends git=1:2.30.2-1+deb11u2 && \
    apt-get -y install --no-install-recommends make=4.3-4.1 && \
    apt-get -y install --no-install-recommends wget=1.21-1+deb11u1 && \
    rm -rf /var/lib/apt/lists/* && \
    python -m pip install --no-cache-dir pip==${PIP_VERSION} && \
    pip install --no-cache-dir poetry==${POETRY_VERSION} && \
    make --directory /app/ install-environment