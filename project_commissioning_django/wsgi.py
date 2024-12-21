"""
WSGI config for project_commissioning_django project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import sys 
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_commissioning_django.settings")
import django 
django.setup()
application = get_wsgi_application()
