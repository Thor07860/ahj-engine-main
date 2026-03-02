web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT app.main:app
release: python init_db_full.py && python -m alembic upgrade head
