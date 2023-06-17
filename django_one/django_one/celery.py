import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_one.settings")

app = Celery("django_one")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

