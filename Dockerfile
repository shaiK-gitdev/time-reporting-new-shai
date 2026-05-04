FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["sh", "-c", "python manage.py migrate --noinput && python -c \"import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE','yh_forms.settings'); import django; django.setup(); from django.contrib.auth.models import User; p=os.environ.get('DJANGO_SUPERUSER_PASSWORD',''); u,_=User.objects.get_or_create(username='admin',defaults={'email':'admin@example.com','is_staff':True,'is_superuser':True}); u.is_staff=True; u.is_superuser=True; u.set_password(p); u.save(); print('Admin ready')\" && python manage.py collectstatic --noinput && gunicorn yh_forms.wsgi:application --bind 0.0.0.0:8080 --workers 2 --timeout 120"]
