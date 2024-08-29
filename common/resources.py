from import_export import resources
from .models import UploadedFile, LogEntry

class UploadedFileResource(resources.ModelResource):
    class Meta:
        model = UploadedFile

class LogEntryResource(resources.ModelResource):
    class Meta:
        model = LogEntry