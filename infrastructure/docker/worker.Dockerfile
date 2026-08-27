FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e .
COPY apps ./apps
COPY packages ./packages
RUN useradd --create-home --uid 10001 appuser && chown -R appuser:appuser /app
USER 10001
CMD ["python","-m","apps.worker.main"]
