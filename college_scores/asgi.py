"""
ASGI config for college_scores project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_scores.settings.develop')

application = get_asgi_application()
