LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-25s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'file',
            'filename': 'debug.log',
            'maxBytes' : 1024*1024*3, # 3mb
            'backupCount': 3,
        }
    },
    'loggers': {
        '': {
            'level': 'ERROR',
            'handlers': ['console', 'file'],
            'propagate': True
        },
        'django.request': {
            'level': 'ERROR',
            'handlers': ['console', 'file']
        }
    }
}
