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

AWS_KEY = 'AKIAIR42QFN63U2ZGSQQ'
AWS_SECRET = '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'

STATIC_ROOT = '/home/ubuntu/mathbreakers.com/static/'
BUYDEBUG=False

os.environ['wsgi.url_scheme'] = 'https'
DEBUG=True
BUYDEBUG = True

ALLOWED_HOSTS = [
	'*',
	'.mathbreakers.com',
	'.mathbreakers.com.',
]

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

MIXPANEL_TOKEN = "8adde2b5cf4754050153990464021fcb"
MIXPANEL_API = "df168bce32e8b36bbede628972d2b5be"
SESSION_COOKIE_DOMAIN = "mathbreakers.com"