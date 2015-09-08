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

STATIC_URL = '//logtacts.s3.amazonaws.com/assets/'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECRET_KEY = get_env_variable("SECRET_KEY")

LOGGING['handlers']['loggly-handler']['address'] = '/dev/log'
LOGGING['loggers']['scripts']['handlers'] = ['loggly-handler']
LOGGING['loggers']['loggly_logs']['handlers'] = ['loggly-handler']