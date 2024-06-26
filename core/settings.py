import os
from pathlib import Path
from django.contrib import messages
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

#load environment variables
load_dotenv(os.path.join(BASE_DIR, ".env"))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-%o2kvbgss&wp^x$_(_y46flfd=bvdzyia1a108$h#t&+%1eu$9'
SECRET_KEY = os.environ.get('SECRET_KEY', 'cg#p$g+j9tax!#a3cup@1$8obt2_+&k3q+pmu)5%asj6yjpkag')
# SECRET_KEY = os.getenv("SECRET_KEY")



# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = os.environ.get('DEBUG', '') != 'False'

ALLOWED_HOSTS = ["*"]
# ALLOWED_HOSTS = ["*.up.railway.app", "127.0.0.1"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authentication',
    'posts',
    'profiles',
    'groups',
    # 'debug_toolbar'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates"), ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
# if DEBUG:
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.postgresql",
#             "NAME": "triply",
#             "USER": "postgres",
#             "PASSWORD": "sweetpoison",
#             "HOST": "localhost"
#         }
#     }


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/


STATIC_URL = "static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "staticfiles/static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Deployment: path to the directory where collectstatic will collect static files for deployment.
# STATIC_ROOT = BASE_DIR/'staticfiles'

# The URL to use when referring to static files (where they will be served from)
# STATIC_URL = '/static/'

# Deployment: Compressed Simplified static file serving using whitenoise.
# https://pypi.org/project/whitenoise/
# reduce the size of the static files when they are served
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# user-uploaded data saved here
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


if DEBUG:
    # email
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "localhost"
    EMAIL_HOST_PASSWORD = ""
    EMAIL_HOST_USER = ""
    EMAIL_PORT = 25
    EMAIL_SSL_CERTFILE = None
    EMAIL_SUBJECT_PREFIX = "[ModernMan]"
    EMAIL_TIMEOUT = None
    EMAIL_USE_LOCALTIME = False
    EMAIL_USE_SSL = False
    EMAIL_USE_TLS = False


# messages
MESSAGE_TAGS = {
    messages.ERROR: "danger",

}


# login url
LOGIN_URL = 'users:login'


# logout redirect
LOGOUT_REDIRECT_URL = LOGIN_URL


# logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },



    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },


    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },

        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_true']
        },

        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(BASE_DIR, 'logs/debug.log'),
        }
    },


    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },

        'django.request': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,

        },

        'django.server': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,

        },

        'modernman_final.custom': {
            'handlers': ['file'],
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'formatter': 'verbose',
            'propagate': True,

        },
    },
}


# DJANGO_LOG_LEVEL = INFO


# custom auth model
AUTH_USER_MODEL = "authentication.CustomUser"


# deploy on heroku
# import django_heroku
# django_heroku.settings(locals())






# deployment
SESSION_COOKIE_SECURE = True


# Deployment: Update database configuration from $DATABASE_URL.
import dj_database_url

DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL, 
            conn_max_age=1800
            ),
        }


DATABASE_URL = os.getenv("DATABASE_URL") 


DATABASES = {
    "default": dj_database_url.config(
        default=DATABASE_URL, 
        conn_max_age=1800
        ),
    }


#     DATABASE_URL = os.getenv("DATABASE_URL")





# During development/for this tutorial you can instead set just the base URL
CSRF_TRUSTED_ORIGINS = ['http://*', 'https://*' ] 


