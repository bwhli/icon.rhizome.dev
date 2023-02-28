FROM python:3.11-buster as venv

ENV POETRY_VERSION=1.3.2
RUN curl -sSL https://install.python-poetry.org | python

WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN python -m venv --copies /app/venv
RUN . /app/venv/bin/activate && ~/.local/share/pypoetry/venv/bin/poetry install --no-root

FROM python:3.11-slim-buster as prod

COPY --from=venv /app/venv /app/venv/
ENV PATH /app/venv/bin:$PATH

WORKDIR /app
COPY ./icon_rhizome_dev /app/icon_rhizome_dev

# Start application
CMD ["gunicorn", "icon_rhizome_dev.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "[::]:8080"]