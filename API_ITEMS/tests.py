import os
import django
from celery.result import AsyncResult

# Configuration de Django pour accéder aux modèles
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Sedadi_API.settings")
django.setup()

from API_ITEMS.tasks import refresh_product_schedules

def test_refresh_product_schedules():
    result = refresh_product_schedules.apply_async()
    print("Task ID:", result.id)
    result.wait()  # Attendez que la tâche soit terminée
    if result.successful():
        print("Task Result:", result.result)
    else:
        print("Task Failed:", result.result)

if __name__ == "__main__":
    test_refresh_product_schedules()
