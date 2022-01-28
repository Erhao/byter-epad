# -*- coding: utf-8 -*-
import logging
from functools import wraps


def singleton(cls):
    """单例类装饰器"""
    instances = {}

    @wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper


def wrap_logger(foo):
    """日志装饰器"""
    logger = logging.getLogger(foo.__name__)

    def inner(*args, **kwargs):
        logger.info(logger.info(f"-----------<{foo.__name__} start>-----------"))
        res = foo(*args, **kwargs)
        logger.info(logger.info(f"-----------<{foo.__name__} end>-----------"))
        return res
    
    return inner