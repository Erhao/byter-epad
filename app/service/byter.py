# -*- coding: utf-8 -*-
from app.db.client import RedisClient
from app.utils import prc_now, hash_key_generator, rds_key_generator
from constants import REALTIME, DATE


rds = RedisClient()


def save_cnt(mac, bid, cnt):
    """
    实时保存cnt到redis

    <bid>_<mac>_<YYYYMMDD>: {
        raw_<hour>_<minute>: <cnt>
    }

    :param mac:
    :param bid:
    :param cnt:
    :return:
    """
    rds_cli = rds()

    now = prc_now()

    rds_key = rds_key_generator(DATE, bid=bid, mac=mac, dt=now)
    hash_key = hash_key_generator(REALTIME, is_raw=True, dt=now)
    print(f"save raw {rds_key} {hash_key} {cnt} to redis")
    rds_cli.hset(rds_key, hash_key, cnt)
