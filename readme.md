# Time Reporting app

This is a docker project to create a container with Python3, Django and Apache2.
In Docker Compose mode container running by with buld in python web server and in producton mode contaier running by apache2 server with mod_wsgi

* docker-compose up -d web

Starts the container named web

* Browse to <http://localhost:8000/>

* One time setup by:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

* Run development server

```bash
python3 manage.py runserver 0.0.0.0:8000
```
