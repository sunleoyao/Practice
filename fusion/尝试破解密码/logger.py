# -*- coding: utf-8 -*-
import logging
import os
from logging import handlers
from conf import settings


def logger(log_file):
    log_level = settings.log_level
    if log_level == 'debug':
        log_level = logging.DEBUG
    elif log_level == 'info':
        log_level = logging.INFO
    elif log_level == 'warning':
        log_level = logging.WARNING
    elif log_level == 'error':
        log_level = logging.ERROR
    else:
        log_level = logging.CRITICAL
    # 1.生成logger对象
    logger = logging.getLogger(log_file)
    logger.setLevel(logging.DEBUG)
    # 2.生成handler对象
    fh = handlers.TimedRotatingFileHandler(filename=os.path.join(settings.LOG_PATH, log_file),
                                           when='D', interval=1, backupCount=3)
    fh.setLevel(log_level)
    # 2.1 把handler对象绑定到logger
    if not logger.handlers:
        logger.addHandler(fh)
    # 3.生成formatter对象
    f = logging.Formatter(fmt='%(asctime)s %(name)s [%(levelname)s] %(message)s', datefmt=None)
    # 3.1 把formatter对象绑定到handler
    fh.setFormatter(f)
    return logger

logger.py