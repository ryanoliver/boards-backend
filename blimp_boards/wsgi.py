"""
WSGI config for blimp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import newrelic.agent


ENVIRONMENT = os.getenv('ENVIRONMENT')

if ENVIRONMENT == 'STAGING':
    settings = 'staging'
elif ENVIRONMENT == 'PRODUCTION':
    settings = 'production'
else:
    settings = 'development'

os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "settings.%s" % settings)

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
application = newrelic.agent.WSGIApplicationWrapper(application)
