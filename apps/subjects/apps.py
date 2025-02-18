"""Subjects app config."""
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from apps.subjects import create_default_groups

class SubjectsConfig(AppConfig):
    """Subjects app config."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.subjects'

    def ready(self):
        post_migrate.connect(create_default_groups, sender=self)
