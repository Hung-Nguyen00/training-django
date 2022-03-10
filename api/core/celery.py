from __future__ import absolute_import, unicode_literals

import os
from api.config.settings import CELERY_BROKER_URL
from celery import Celery
from kombu import Queue

# set the default Django settings module for the 'celery' program.
# this is also used in manage.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.config.settings.settings")


app = Celery("sk-softchecker-v3")

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.ONCE = {
  'backend': 'celery_once.backends.Redis',
  'settings': {
    'url': CELERY_BROKER_URL,
    'default_timeout': 60 * 1
  }
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.broker_url = CELERY_BROKER_URL
