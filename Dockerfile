FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Initialize database, run migrations, then start the app
CMD ["bash", "-c", "python init_db_full.py && alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]