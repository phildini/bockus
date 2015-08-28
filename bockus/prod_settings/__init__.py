from bockus.settings import *
import dj_database_url

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES['default'] = dj_database_url.config()

ALLOWED_HOSTS = [
    '.booksonas.com',
    'localhost',
    '127.0.0.1',
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECRET_KEY = get_env_variable("SECRET_KEY")

STATIC_URL = 'https://media.quailcomics.com/assets/'

LOGGING['handlers']['loggly-handler']['address'] = '/dev/log'
LOGGING['loggers']['scripts']['handlers'] = ['loggly-handler']
LOGGING['loggers']['loggly_logs']['handlers'] = ['loggly-handler']