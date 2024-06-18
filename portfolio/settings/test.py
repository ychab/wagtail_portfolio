from tempfile import gettempdir

from .base import *

INSTALLED_APPS += [
    # Well... @see https://github.com/wagtail/wagtail/issues/1824
    'wagtail.contrib.search_promotions',
]

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

# Boost perf a little
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

STATIC_ROOT = os.path.join(gettempdir(), 'portfolio', 'static')
MEDIA_ROOT = os.path.join(gettempdir(), 'portfolio', 'media')

WAGTAILADMIN_BASE_URL = "http://127.0.0.1:8000"

try:
    from .local import *
except ImportError:
    pass
