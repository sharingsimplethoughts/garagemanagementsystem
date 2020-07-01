# from __future__ import absolute_import, unicode_literals
# import os
# from celery import Celery
#
# # set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notifications_post.settings')
#
# app = Celery('notifications_post')
#
# # Using a string here means the worker doesn't have to serialize
# # the configuration object to child processes.
# # - namespace='CELERY' means all celery-related configuration keys
# #   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace='CELERY')
#
# # Load task modules from all registered Django app configs.
# app.autodiscover_tasks()
from __future__ import absolute_import
import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Garage.settings')

app = Celery('Garage' ,backend='amqp',broker='amqp://sukamalsinha@localhost//')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
