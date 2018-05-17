"""
Django settings for AuditSQL project.
Generated by 'django-admin startproject' using Django 2.0.2.
For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import sys

import djcelery
import logging
import ldap
from celery.schedules import crontab
from django_auth_ldap.config import LDAPSearch

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*6stzec#)2qc&is59g1=#)9mccyjbxcl1(s-dti@!m1oz*c-kv'

# Define apps path
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Define user auth table
AUTH_USER_MODEL = 'user_manager.UserAccount'

# Define login page
LOGIN_URL = '/users/login/'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'djcelery',
    'kombu.transport.django',
    'user_manager',
    'project_manager',
    'mstats',
    'scheduled_tasks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'AuditSQL.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'AuditSQL.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# 配置数据库信息
# 存储审核系统的表结构和数据
# 修改成自己的数据库地址
# 权限：grant all privileges on auditsql.* to xxx
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'auditsql',
        'USER': 'root',
        'HOST': 'localhost',
        'PASSWORD': '123.com',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4'
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

# Enable ldap backend support
AUTHENTICATION_BACKENDS = [
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

# 存放静态文件
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '/static/')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# 存放上传文件
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 使用redis缓存session
SESSION_ENGINE = "django.contrib.sessions.backends.cache"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# celery for redis
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'

# 使用数据库来存放定时任务记录
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

# django-channels配置
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

# 配置ASGI
ASGI_APPLICATION = "AuditSQL.routing.application"


# LDAP配置
# 若不使用LDAP进行认证，注释上面的'django_auth_ldap.backend.LDAPBackend'
# ldap 服务器地址
AUTH_LDAP_SERVER_URI = "ldap://XXX.NET"
# AUTH_LDAP_START_TLS = True
AUTH_LDAP_ALWAYS_UPDATE_USER = True
# ldap绑定用户名，用户所在的绝对路径
AUTH_LDAP_BIND_DN = "CN=lazzyfu,OU=xx,DC=xx,DC=xx"
# ldap绑定用户名的密码
AUTH_LDAP_BIND_PASSWORD = "123.com"
# 搜索
AUTH_LDAP_USER_SEARCH = LDAPSearch("OU=xx科技,OU=xxx集团,DC=XXX,DC=NET", ldap.SCOPE_SUBTREE, "(CN=%(user)s)")

# 下面字段必须存在
# username：用户名
# email：邮箱地址
# displayname：对应的昵称或中文名
# key：为数据库字段
# value：为ldap对应字段
AUTH_LDAP_USER_ATTR_MAP = {"username": "cn", 'email': 'mail', "displayname": 'displayName'}

# 若需要调试ldap，不注释下面代码
# logger = logging.getLogger('django_auth_ldap')
# logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.DEBUG)


# inception服务地址
INCEPTION_HOST = '127.0.0.1'
INCEPTION_PORT = 6033

# inception备份功能数据库地址
# 和inception配置文件中指定的inception_remote_backup_host、inception_remote_system_user、inception_remote_backup_port
# inception_remote_system_password一致
INCEPTION_BACKUP_HOST = '127.0.0.1'
INCEPTION_BACKUP_USER = 'root'
INCEPTION_BACKUP_PASSWORD = '123.com'
INCEPTION_BACKUP_PORT = 3306

# 邮箱账号
# 修改成自己邮箱账户
# 该账户用于实时推送审核邮件
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'lazzyfu'
EMAIL_HOST_PASSWORD = '123.com'
EMAIL_USE_TLS = False
EMAIL_FROM = 'lazzyfu@163.com'

# 日志
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {  # 日志格式
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'}
    },
    'handlers': {  # 处理器
        'file': {  # 记录到日志文件(需要创建对应的目录，否则会出错)
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/all.log',  # 日志输出文件
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份份数
            'formatter': 'standard',  # 使用哪种formatters日志格式
        },
        'console': {  # 输出到控制台
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {  # logging管理器
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False
        },
        'django.request': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}