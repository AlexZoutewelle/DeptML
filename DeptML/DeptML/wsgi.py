"""
WSGI config for DeptML project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DeptML.settings')

#Code die wordt gerund on startup hier?




from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

