from .base import *

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

for logger in LOGGING['loggers'].values():
    if 'django.server' not in logger['handlers']:
        logger['handlers'] += ['django.server']

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# Javascript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/2.1/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

try:
    from .local import *  # isort:skip
except ImportError:
    pass  # NOQA
