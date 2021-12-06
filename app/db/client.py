# -*- coding: utf-8 -*-
import os
import redis
from dotenv import load_dotenv


class RedisClient(object):
    def __init__(self):
        load_dotenv(".env")
        self.host = os.getenv('REDIS_HOST')
        self.port = os.getenv('REDIS_PORT')
        self.pwd = os.getenv('REDIS_PASS')
        self.client = None

    def __call__(self, *args, **kwargs):
        self.connect_redis()
        return self.client

    def connect_redis(self):
        self.client = redis.Redis(host=self.host, port=self.port, password=self.pwd, decode_responses=True)


redis_client = RedisClient()
