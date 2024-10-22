import logging
import logging.config
import copy
import os
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
log_filename = f"log_{timestamp}.log"

log_dir = "logs"

if not os.path.exists(log_dir):
    os.makedirs(log_dir)
    
log_path = os.path.join(log_dir, log_filename)

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
            'filename': f'{log_path}',
            'class': 'logging.FileHandler',
            'formatter': 'standard',
            'mode': 'w'
        }
    },
    'loggers': {
        'node_log': {
            'handlers': ['file_handler',],
            'level': 'INFO',
            'propagate': False
        },
    }
}
logging.config.dictConfig(log_dict)
    
    
def get_logger():
   
   return logging.getLogger('node_log')

