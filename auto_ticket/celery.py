"""A module of celery configurations"""
import os
from celery import Celery
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auto_ticket.settings')
app = Celery('auto_ticket')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
