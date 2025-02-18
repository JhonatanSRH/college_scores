"""Subjects module"""
import logging as log
from django.db import IntegrityError

def create_default_groups(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    from apps.subjects.models import Subject, Registration
    teachers_group, __ = Group.objects.get_or_create(name="teachers")
    students_group, __ = Group.objects.get_or_create(name="students")
    try:
        content_type = ContentType.objects.get_for_models(Subject, Registration)
        permissions = Permission.objects.filter(content_type=content_type[Subject])
        teachers_group.permissions.set(permissions)
        permissions = Permission.objects.filter(content_type=content_type[Registration])
        students_group.permissions.set(permissions)
    except IntegrityError:
        log.error("Data migration couldn't be completed")
