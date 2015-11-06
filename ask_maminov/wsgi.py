"""
WSGI config for ask_maminov project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os, sys
from django.core.wsgi import get_wsgi_application

#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ask_maminov.settings")

#print(os.environ['DJANGO_SETTINGS_MODULE'].split(os.pathsep))

application = get_wsgi_application()