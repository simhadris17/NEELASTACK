FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e .
COPY apps ./apps
COPY packages ./packages
COPY .env.example ./.env.example
COPY alembic.ini ./
COPY alembic ./alembic
RUN useradd --create-home --uid 10001 appuser && chown -R appuser:appuser /app
USER 10001
EXPOSE 8000
CMD ["python","-m","apps.api.start"]
