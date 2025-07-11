import os
from pathlib import Path
import environ

# Load environment variables from .env file
env = environ.Env()
environ.Env.read_env(Path(__file__).resolve().parent.parent / '.env')

# Base directory of the projectfrom pathlib import Path
# Build paths inside the project like this: BASE_DIR / 'subdir'
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY='django-insecure-s%ze&ormldy6e8i8(k84(0btyz!#ubj40-16*1svrh^uoc96c+'

# API and other important info
VTPass_API_KEY=env('VTPass_API_KEY')
VTPass_PUBLIC_KEY=env('VTPass_PUBLIC_KEY')
VTPass_SECRET_KEY=env('VTPass_SECRET_KEY')
VTPass_BASE_URL=env('VTPass_BASE_URL')
VTPass_EMAIL=env('VTPass_EMAIL')  # Replace with your Vtpass email
VTPass_PASSWORD=env('VTPass_PASSWORD')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []#'sheltrade.godhouse.org', 'https://www.sheltrade.godhouse.org', 'www.sheltrade.godhouse.org', 'sheltrade.pythonanywhere.com', 'https://www.sheltrade.pythonanywhere.com', 'www.sheltrade.pythonanywhere.com']

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    "django.contrib.humanize",
    
    # my apps
    'billPayments',
    'contact',
    'core',
    'crypto',
    'giftcard',
    'mobileTopUp',
    'sheltradeAdmin',
    'wallet',

    # third-party apps
    # 'djmoney',
    'corsheaders',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'django_countries',
    'phonenumber_field',
    'mptt',
    'tinymce',
    # 'guardian',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    
    # corsheaders specific middleware
    "corsheaders.middleware.CorsMiddleware",
    
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # my apps middleware
    'core.middleware.RequestMiddleware',

    # allauth specific middleware
    'allauth.account.middleware.AccountMiddleware',
]


ROOT_URLCONF = 'sheltrade.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "core.context_processors.currency",
                "core.context_processors.UserProfile",
                "core.context_processors.countries",
                "sheltradeAdmin.context_processors.details",
                "contact.context_processors.base_template",
                "contact.context_processors.sheltrade_info",
                # "django.core.context_processors.request",
                # 'allauth.account.context_processors.account',
                # "allauth.socialaccount.context_processors.socialaccount",

            ],
        },
    },
]

WSGI_APPLICATION = 'sheltrade.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = 'static/'
STATICFILES_DIRS= [BASE_DIR / 'static']
STATIC_ROOT = 'staticfiles'

MEDIA_URL = '/media/'  # Add a leading slash for correct URL path
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',

    # This enables the Guardian backend.
    # 'guardian.backends.ObjectPermissionBackend',
]



SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile'],
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time',
        ]
    }
}

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'APP': {
            'client_id': '74765500020-gi7u5q1nmani6kemv428ckn936k4bncd.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        }
    },
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile'],
        'APP': {
            'client_id': '509697181767177',
            'secret': '651a9335cb086c9c8d5fca07d71f1a86',
            'key': ''
        }
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'myappsa9@gmail.com'
EMAIL_HOST_PASSWORD = 'fnjj frry egqv feyg'
DEFAULT_FROM_EMAIL = 'myappsa9@gmail.com'

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8081",
    "http://localhost:8082",
    "http://127.0.0.1:8081",
    "http://127.0.0.1:8082",
    "http://10.0.2.2:8000",
    "exp://192.168.43.203:8081",
    "exp://192.168.43.203:8082",
]

CORS_ALLOW_ALL_ORIGINS = True


LOGIN_URL = '/accounts/login/'
SIGNUP_URL = '/accounts/signup/'
LOGIN_REDIRECT_URL = '/dashboard/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'


#ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "optional" #"mandatory"
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = False
#ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_LOGIN_METHODS = {'email', 'username'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']

ACCOUNT_EMAIL_SUBJECT_PREFIX = "Sheltrade "


TINYMCE_DEFAULT_CONFIG = {
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'silver',
    'plugins': '''
            textcolor save link image media preview codesample contextmenu
            table code lists fullscreen  insertdatetime  nonbreaking
            contextmenu directionality searchreplace wordcount visualblocks
            visualchars code fullscreen autolink lists  charmap print  hr
            anchor pagebreak
            ''',
    'toolbar1': '''
            fullscreen preview bold italic underline | fontselect,
            fontsizeselect  | forecolor backcolor | alignleft alignright |
            aligncenter alignjustify | indent outdent | bullist numlist table |
            | link image media | codesample |
            ''',
    'toolbar2': '''
            visualblocks visualchars |
            charmap hr pagebreak nonbreaking anchor |  code |
            ''',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True,
}

