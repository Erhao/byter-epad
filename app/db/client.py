# -*- coding: utf-8 -*-
import os
import redis
from dotenv import load_dotenv

from app.decorator import singleton


@singleton
class RedisClient(object):
    def __init__(self):
        load_dotenv(".env")
        self.host = os.getenv('REDIS_HOST', '127.0.0.1')
        self.port = int(os.getenv('REDIS_PORT', 6379))
        self.pwd = os.getenv('REDIS_PASS')
        self.client = None

    def __call__(self, *args, **kwargs):
        self.connect_redis()
        return self.client

    def connect_redis(self):
        self.client = redis.Redis(host=self.host, port=self.port, password=self.pwd, decode_responses=True)
