"""
WSGI config for momentsoflife_server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import multiprocessing

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'momentsoflife_server.settings')

application = get_wsgi_application()

bind = "127.0.0.1:8000"
workers = 2