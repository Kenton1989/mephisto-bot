import re
from nonebot.default_config import *
import logging

LOG_CONFIG = {
    'filename': 'qqbot.log',
    'level': logging.WARNING,
    'format': '%(asctime)s %(name)-15s %(levelname)-8s %(message)s',
}

log_handler = logging.FileHandler(LOG_CONFIG['filename'], encoding='utf-8')
log_handler.setLevel(LOG_CONFIG['level'])
log_handler.setFormatter(logging.Formatter(LOG_CONFIG['format']))

logging.basicConfig(handlers=[log_handler])

SUPERUSERS = {}
COMMAND_START = [re.compile(r'[/!／！]')]

ACCESS_TOKEN = ''

HOST = 'localhost'
PORT = 44444
