release: cd core && python manage.py migrate --noinput
web: cd core && gunicorn core.wsgi:application --bind 0.0.0.0:${PORT:-8000}
