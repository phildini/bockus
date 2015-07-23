from bockus.settings import *
import dj_database_url

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES['default'] = dj_database_url.config()

ALLOWED_HOSTS = [
    '.booksonas.com',
    '.herokuapp.com',
    'localhost',
    '127.0.0.1',
]

SECRET_KEY = get_env_variable("SECRET_KEY")

INSTALLED_APPS += (
    'gunicorn',
)