DATABASES = {
    'default': {
        'ENGINE': 'django_tidb',
        'NAME': 'django_tests',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': 4000,
    },
    'other': {
        'ENGINE': 'django_tidb',
        'NAME': 'django_tests',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': 4000,
    },
}
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
USE_TZ = False
SECRET_KEY = 'django_tests_secret_key'
