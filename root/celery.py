import os
from celery import Celery

# Django settings faylini aniqlab qo‘yamiz
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')

app = Celery('root')

# Django settingsdan CELERY_* sozlamalarni yuklaydi
app.config_from_object('django.conf:settings', namespace='CELERY')

# Barcha Django app’lar ichidan tasks.py fayllarni avtomatik qidiradi
app.autodiscover_tasks()