# API_FILES/tasks.py
from celery import shared_task
import logging
from .models import UploadedFile, ParsedData
from .API_FILES_signals import parse_file

logger = logging.getLogger('api_files')

@shared_task
def parse_uploaded_file(file_id):
    try:
        uploaded_file = UploadedFile.objects.get(id=file_id)
        parse_file(UploadedFile, uploaded_file)
    except UploadedFile.DoesNotExist:
        logger.error(f"UploadedFile with ID {file_id} does not exist.")

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def delete_uploaded_files_in_batches(self, file_ids, batch_size=5000):
    logger.info(f"Starting delete_uploaded_files_in_batches task with batch size {batch_size}")
    try:
        process_deletion_batches(UploadedFile, file_ids, batch_size)
        logger.info("Completed delete_uploaded_files_in_batches task")
    except Exception as e:
        logger.error(f"Error in delete_uploaded_files_in_batches task: {e}")

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def delete_parsed_data_in_batches(self, file_ids, batch_size=5000):
    logger.info(f"Starting delete_parsed_data_in_batches task with batch size {batch_size}")
    try:
        process_deletion_batches(ParsedData, file_ids, batch_size)
        logger.info("Completed delete_parsed_data_in_batches task")
    except Exception as e:
        logger.error(f"Error in delete_parsed_data_in_batches task: {e}")

def process_deletion_batches(model, file_ids, batch_size):
    total_deleted = 0
    total_objects = len(file_ids)
    logger.info(f"Total {model.__name__} objects to delete: {total_objects}")

    for start in range(0, total_objects, batch_size):
        end = min(start + batch_size, total_objects)
        batch = file_ids[start:end]
        model.objects.filter(id__in=batch).delete()
        total_deleted += len(batch)
        logger.info(f"Deleted batch of {len(batch)} {model.__name__} objects. Total deleted so far: {total_deleted}")

    logger.info(f"Completed deletion of {model.__name__} objects. Total deleted: {total_deleted}")
