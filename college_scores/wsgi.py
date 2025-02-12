"""
WSGI config for college_scores project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_scores.settings.develop')

application = get_wsgi_application()
