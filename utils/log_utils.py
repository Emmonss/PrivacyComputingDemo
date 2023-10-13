from utils.constant_utils import LOG_WHEN,LOG_INTERVAL,LOG_DIR,\
                LOG_BACKUP,LOG_FILE_LEVEL,LOG_SCREEN_LEVEL,LOG_PLATFORM_LEVEL

from utils.date_utils import get_now_time_str


import logging
import os
from logging import handlers

LEVEL_MAP ={}



DEFAULT_FORMAT = ''
ALG_FORMAT = ''

class Logger:
    def create(self):
        pass