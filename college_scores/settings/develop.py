"""Develop settings."""
from college_scores.settings.base import *


DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': env('DB_NAME'),
    }
}
