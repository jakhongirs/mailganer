import os

import environ
from celery import Celery
from django.conf import settings

env = environ.Env()
env.read_env(f"{os.getcwd()}/.env")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", env.str("DJANGO_SETTINGS_MODULE"))

app = Celery("core")
app.autodiscover_tasks(packages=settings.INSTALLED_APPS)
app.conf.broker_connection_retry_on_startup = True
