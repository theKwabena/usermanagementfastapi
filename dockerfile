FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /home/app
COPY ./pyproject.toml ./poetry.lock* ./

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 &&\
    cd /usr/local/bin  && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create

RUN poetry install

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


