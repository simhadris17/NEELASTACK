@echo off
python -m uvicorn apps.api.main:app --reload --port 8000
