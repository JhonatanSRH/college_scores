"""Subjects app admin."""
from django.contrib import admin
from apps.subjects.models import Subject, Registration

admin.site.register(Subject)
admin.site.register(Registration)
