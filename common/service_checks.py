# common/service_checks.py
import logging
import psutil
from django.db import connection

logger = logging.getLogger('common')

def check_service_availability():
    logger.info("Starting service availability check...")
    
    # Vérification de la connectivité de la base de données
    database_error = check_database_connection()
    if database_error:
        logger.error(f"Service unavailable due to database connection: {database_error}")
        return database_error

    # Vérification de la surcharge du serveur
    server_load_error = check_server_load()
    if server_load_error:
        logger.error(f"Service unavailable due to server load: {server_load_error}")
        return server_load_error

    logger.info("All services are available.")
    return None

def check_database_connection():
    logger.info("Checking database connection...")
    
    try:
        connection.ensure_connection()
        logger.info("Database connection is available.")
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        return "Database connection error"

    return None

def check_server_load():
    server_load = get_server_load()
    logger.info(f"Current server load: {server_load:.2f} per CPU")
    
    if server_load > 0.9:
        logger.error(f"Server is overloaded with load {server_load:.2f} per CPU")
        return "Server is overloaded"

    logger.info("Server load is within acceptable range.")
    return None

def get_server_load():
    """
    Récupère la charge moyenne du serveur par CPU sur 1 minute.
    """
    load1, load5, load15 = psutil.getloadavg()
    cpu_count = psutil.cpu_count()
    load_per_cpu = load1 / cpu_count
    return load_per_cpu
