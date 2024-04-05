from .base import *

DATABASES['default'].update({
    'HOST': 'db',  # Docker 内の PostgreSQL サービスの名前
})
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'host.docker.internal']
