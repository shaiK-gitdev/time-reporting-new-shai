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

CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py createsuperuser --noinput --username admin --email admin@example.com || true && python manage.py collectstatic --noinput && gunicorn yh_forms.wsgi:application --bind 0.0.0.0:8080 --workers 2 --timeout 120"]
