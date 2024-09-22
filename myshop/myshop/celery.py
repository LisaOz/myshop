import os
from celery import Celery

"""
This file provides Celery instance configuration for the project.
"""

# Set the default Django settings module for the celery program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings') # set variable for the Celery command-line program

app = Celery('myshop') # create an instance of the application
app.config_from_object('django.conf:settings', namespace='CELERY') # load any custom configuration from the project settings. Celery namespace setting is needed
app.autodiscover_tasks() # tell celery to auto-discover asynchronous tasks for the application. Celery looks for a tasks.py file in each app directory of apps added to INSTALLED_APP and load asynchronous tasks defined in it

