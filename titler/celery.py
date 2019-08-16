import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "titler.settings")

app = Celery('titler')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.update({
    'timezone': 'Asia/Krasnoyarsk',
    'broker_url': 'filesystem://',
    'broker_transport_options': {
        'data_folder_in': '.broker/out',
        'data_folder_out': '.broker/out',
        'data_folder_processed': '.broker/processed'
    }})
app.autodiscover_tasks()
