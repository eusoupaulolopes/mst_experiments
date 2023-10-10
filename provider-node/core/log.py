import logging
import logging.config
import copy

log_dict = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(threadName)s - [%(levelname)s] %(uuid)s, %(message)s'
        },
        'slow': {
            'format': '%(asctime)s - %(threadName)s - [%(levelname)s], %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'slow',
            'class': 'logging.StreamHandler',
        },
        'file_handler': {
            'level': 'INFO',
            'filename': 'core.log',
            'class': 'logging.FileHandler',
            'formatter': 'standard',
            'mode': 'w'
        }
    },
    'loggers': {
        'core': {
            'handlers': ['file_handler',],
            'level': 'INFO',
            'propagate': False
        },
    }
}
logging.config.dictConfig(log_dict)

def get_logger():
   
    return logging.getLogger('core')