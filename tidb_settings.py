DATABASES = {
    'default': {
        'ENGINE': 'django_tidb',
        'NAME': 'django_tests',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': 4000,
    },
}
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
USE_TZ = False