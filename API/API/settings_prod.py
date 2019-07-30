from .settings import *
import dj_database_url


DEBUG = False


# procura pela URL do banco em DATABASE_URL
DATABASES = {
    'default': dj_database_url.config()
}


# Heroku Statics Hack (não é muito recomendado para produção!!)
# https://devcenter.heroku.com/articles/django-assets

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


EMAIL_HOST = str(os.environ.get('EMAIL_HOST'))
EMAIL_HOST_USER = str(os.environ.get('EMAIL_HOST_USER'))
EMAIL_HOST_PASSWORD = str(os.environ.get('EMAIL_HOST_PASSWORD'))
EMAIL_PORT = int(os.environ.get('EMAIL_PORT'))
EMAIL_USE_TLS = bool(int(os.environ.get('EMAIL_USE_TLS')))
EMAIL_USE_SSL = bool(int(os.environ.get('EMAIL_USE_SSL')))
