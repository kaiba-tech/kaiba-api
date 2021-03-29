FROM tiangolo/uvicorn-gunicorn:python3.8-slim

ENV PYTHONUNBUFFERED True

RUN pip install poetry

WORKDIR /app
COPY poetry.lock pyproject.toml /app/


RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

COPY ./kaiba_api /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "$PORT"]
