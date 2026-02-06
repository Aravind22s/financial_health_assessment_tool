"""
ASGI config for sme_platform project.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sme_platform.settings')
application = get_asgi_application()
