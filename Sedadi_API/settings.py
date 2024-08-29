# settings.py
import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from celery.schedules import crontab

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(z$=@brnz*-@+g$=!s&@z*v)ln6=(qhb&pjw_mx!$2u2$%_z'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['corak-esl.tech', 'www.corak-esl.tech', '212.227.119.232', '192.168.119.140', '192.168.119.141', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'API_FILES.apps.ApiFilesConfig',
    'API_ITEMS.apps.ApiItemsConfig',
    'ardoise',
    'common',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
    'Corak_ESL.apps.CorakEslConfig',
    'custom_user_management',
    'django_celery_beat',
    'import_export',
    'axes',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # 'common.middleware.LoadLogsMiddleware',
    'Sedadi_API.middleware.SwaggerLoggingMiddleware',
    'axes.middleware.AxesMiddleware',

]

ROOT_URLCONF = 'Sedadi_API.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Sedadi_API.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# User étendu
# AUTH_USER_MODEL = 'users.Magasin'

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'

# Ajout des chemins pour les fichiers statiques
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Chemin où les fichiers statiques seront collectés via 'collectstatic'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S,%f',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'api_files_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'api_files.log'),
            'formatter': 'verbose',
            'maxBytes': 10 * 1024 * 1024,  # 10 MB
            'backupCount': 5,
        },
        'api_items_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'api_items.log'),
            'formatter': 'verbose',
            'maxBytes': 10 * 1024 * 1024,  # 10 MB
            'backupCount': 5,
        },
        'ardoise_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'ardoise.log'),
            'formatter': 'verbose',
            'maxBytes': 10 * 1024 * 1024,  # 10 MB
            'backupCount': 5,
        },
        'common_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'common.log'),
            'formatter': 'verbose',
            'maxBytes': 10 * 1024 * 1024,  # 10 MB
            'backupCount': 5,
        },
        'corak_esl_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'corak_esl.log'),
            'formatter': 'verbose',
            'maxBytes': 10 * 1024 * 1024,  # 10 MB
            'backupCount': 5,
        },
        'custom_user_management_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'custom_user_management.log'),
            'formatter': 'verbose',
            'maxBytes': 10 * 1024 * 1024,  # 10 MB
            'backupCount': 5,
        },
        'celery_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'celery.log'),
            'formatter': 'verbose',
            'maxBytes': 10 * 1024 * 1024,  # 10 MB
            'backupCount': 5,
        },
        'swagger_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'swagger.log'),
            'formatter': 'verbose',
            'maxBytes': 10 * 1024 * 1024,  # 10 MB
            'backupCount': 5,
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'api_files': {
            'handlers': ['api_files_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'api_items': {
            'handlers': ['api_items_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'ardoise': {
            'handlers': ['ardoise_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'common': {
            'handlers': ['common_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'corak_esl': {
            'handlers': ['corak_esl_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'custom_user_management': {
            'handlers': ['custom_user_management_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'celery': {
            'handlers': ['celery_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'swagger': {
            'handlers': ['swagger_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

CSRF_TRUSTED_ORIGINS = [
    'https://corak-esl.tech',
    # Ajoutez d'autres origines si nécessaire
]

DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000000  # Augmentez cette valeur selon vos besoins

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'common.authentication.CustomTokenAuthentication',
    ),
}

CELERY_TASK_DEFAULT_RETRY_DELAY = 60
CELERY_TASK_MAX_RETRIES = 3
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_REJECT_ON_WORKER_LOST = True

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Paris'

CELERY_BEAT_SCHEDULE = {
    'refresh-product-schedules-every-day': {
        'task': 'API_ITEMS.tasks.refresh_product_schedules',
        'schedule': crontab(hour=3, minute=0),
    },
    'test-check-and-update-promotions-task': {
       'task': 'API_ITEMS.tasks.test_check_and_update_promotions',
       'schedule': crontab(minute='*/5'),
    },
}


AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',  # Ajoutez cette ligne
    'django.contrib.auth.backends.ModelBackend',  # Conservez le backend Django par défaut
]

# Autres configurations nécessaires
AXES_LOCKOUT_TEMPLATE = 'lockout.html'  # Template à utiliser pour les lockouts
AXES_RESET_ON_SUCCESS = True  # Réinitialiser le compteur de tentatives après une connexion réussie

#Axes Config
AXES_FAILURE_LIMIT = 5  # Nombre de tentatives de connexion avant blocage
AXES_COOLOFF_TIME = 1  # Temps de blocage en heures