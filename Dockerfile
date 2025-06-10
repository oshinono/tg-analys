FROM python:3.12-alpine

WORKDIR /app

COPY pyproject.toml .

RUN pip install uv
RUN uv sync

COPY alembic.ini .
COPY alembic alembic

COPY src src

CMD ["sh", "-c", "uv run alembic upgrade head && uv run python src/main.py"]