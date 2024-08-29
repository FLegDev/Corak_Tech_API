import os
import logging
from django.core.management.base import BaseCommand
from common.models import LogEntry, LogFilePosition
from datetime import datetime

logger = logging.getLogger(__name__)

LOG_FILES = {
    'API_FILES': '/home/DeveloppementOnline/logs/api_files.log',
    'API_ITEMS': '/home/DeveloppementOnline/logs/api_items.log',
    'ARDOISE': '/home/DeveloppementOnline/logs/ardoise.log',
    'COMMON': '/home/DeveloppementOnline/logs/common.log',
    'CELERY_TASKS': '/home/DeveloppementOnline/logs/celery_tasks.log',
    'CELERY': '/home/DeveloppementOnline/logs/celery.log',
    'CORAK_ESL': '/home/DeveloppementOnline/logs/corak_esl.log',
    'CUSTOM_USER_MANAGEMENT': '/home/DeveloppementOnline/logs/custom_user_management.log',
    'DJANGO_ERROR': '/home/DeveloppementOnline/logs/django_error.log',
    'DJANGO': '/home/DeveloppementOnline/logs/django.log',
}

class Command(BaseCommand):
    help = 'Load logs into the database'

    def handle(self, *args, **options):
        for app_name, log_file_path in LOG_FILES.items():
            if not os.path.exists(log_file_path):
                logger.error(f'Log file {log_file_path} does not exist')
                continue

            self.load_new_logs(app_name, log_file_path)

    def load_new_logs(self, app_name, log_file_path):
        log_file_position, created = LogFilePosition.objects.get_or_create(log_file=log_file_path)
        current_position = log_file_position.position

        with open(log_file_path, 'r') as log_file:
            log_file.seek(current_position)
            for line in log_file:
                try:
                    level, timestamp, message = self.parse_log_line(line)
                    LogEntry.objects.create(
                        application=app_name,
                        level=level,
                        message=message,
                        timestamp=timestamp
                    )
                except Exception as e:
                    logger.error(f'Failed to parse log line: {line} - Error: {e}')
                current_position += len(line)

        log_file_position.position = current_position
        log_file_position.save()

    def parse_log_line(self, line):
        parts = line.split(' ', 4)
        if len(parts) < 5:
            raise ValueError('Log line does not have enough parts')
        level = parts[0]
        timestamp_str = parts[1] + ' ' + parts[2]
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')
        message = parts[4].strip()
        return level, timestamp, message
