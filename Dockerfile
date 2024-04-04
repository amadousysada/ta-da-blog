# syntax=docker/dockerfile:1
FROM python:3.10 as build

ARG CI_COMMIT_SHA
ARG CI_BUILD_REF_SLUG

ARG USERNAME="app"


ENV CI_COMMIT_SHA $CI_COMMIT_SHA
ENV CI_BUILD_REF_SLUG $CI_BUILD_REF_SLUG

ENV PATH="/root/.local/bin:/root/.poetry/bin:${PATH}" \
    SHELL="/bin/bash" \
    PYTHONUNBUFFERED=1

# Create user app and create app directory
RUN useradd -ms /bin/bash ${USERNAME} && \
    mkdir /app/ && chown ${USERNAME}:${USERNAME} /app/


COPY --chown=app:app tada /app/tada
COPY --chown=app:app tada/alembic /app/alembic
COPY --chown=app:app tada/alembic/alembic.ini /app/alembic.ini
COPY --chown=app:app .bandit poetry.lock pyproject.toml /app/

RUN curl -sSL https://install.python-poetry.org | python - && \
	poetry config virtualenvs.create false && \
	poetry config virtualenvs.in-project false

WORKDIR /app/

FROM build as dev

RUN poetry install

COPY --chown=app:app pytest.ini /app/

EXPOSE 8001
EXPOSE 8081
