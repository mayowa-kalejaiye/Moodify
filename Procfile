release: python scripts/setup_production_db.py && python manage.py collectstatic --noinput
web: gunicorn mood_tracker.wsgi
