from .base import *

DATABASES['default'].update({
    'HOST': 'localhost',
})
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
