import os
TEMPLATE_DIRS = (
    "/home/ubuntu/mathbreakers.com/mathbreakers/templates/",
)

STATICFILES_DIRS = (
    '/home/ubuntu/mathbreakers.com/static2/',
)

MEDIA_ROOT = '/home/ubuntu/mathbreakers.com/media/'

DATABASES = { 
   'default': {
       'ENGINE': 'django.db.backends.mysql',
       'NAME': 'mathbreakers',
       'USER': 'morgan',
       'PASSWORD': '19tpfidrisoomd17',
       'HOST': 'mathbreakers-db.cbvvbhhqy7gr.us-west-1.rds.amazonaws.com',
       'PORT': '3306',
   }   
}

DEFAULT_FROM_EMAIL = "robot@mathbreakers.com"
SERVER_EMAIL = "robot@mathbreakers.com"


AWS_KEY = 'AKIAIR42QFN63U2ZGSQQ'
AWS_SECRET = '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'

EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
EMAIL_HOST_USER='AKIAJF6OPDLVPDDH3RYQ'
EMAIL_HOST_PASSWORD='AvCs+pHTXRxefNfPKuYtAWeFMVvUOKGjugmv2nyYs21u'
EMAIL_USE_TLS=True

STATIC_ROOT = '/home/ubuntu/mathbreakers.com/static/'
BUYDEBUG=False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django.log',
        },
        'mail_admins': {
            'level': 'ERROR',
            #'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'mathbreakers': {
            'handlers': ['file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        }
    },
}

os.environ['wsgi.url_scheme'] = 'https'
DEBUG=False
TEMPLATE_DEBUG=False
BUYDEBUG = False

ALLOWED_HOSTS = [
	'*',
	'.mathbreakers.com',
	'.mathbreakers.com.',
]

MIXPANEL_TOKEN = "91c9b13e54792a4490d41f397c14b62d"
MIXPANEL_API = "0989edf83ec25a0ff512bb5802b4a67b"
SESSION_COOKIE_DOMAIN = "mathbreakers.com"