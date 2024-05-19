# start app
python manage.py runserver

# start celery server

## For Windows
celery -A shift_scheduler worker --loglevel=info -P solo
## For other OS
celery -A shift_scheduler worker --loglevel=info

# Start Celery Beat
celery -A shift_scheduler beat -l info -S django
