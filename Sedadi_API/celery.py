from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
import logging
from celery.utils.log import get_task_logger

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Sedadi_API.settings')

app = Celery('Sedadi_API')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: [n.name for n in settings.INSTALLED_APPS if hasattr(n, 'name')])

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'
app.conf.beat_schedule = {
    'refresh-product-schedules-every-day': {
        'task': 'API_ITEMS.tasks.refresh_product_schedules',
        'schedule': crontab(hour=1, minute=0),
        'args': ()
    },
}

app.conf.timezone = 'Europe/Paris'
app.conf.broker_connection_retry_on_startup = True
app.conf.task_default_retry_delay = 60
app.conf.task_max_retries = 5
app.conf.result_backend = 'redis://localhost:6379/0'
app.conf.task_default_queue = 'default'

logger = get_task_logger(__name__)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s %(asctime)s %(module)s %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(settings.BASE_DIR, 'logs', 'celery.log'))
    ]
)

if __name__ == '__main__':
    app.start()
