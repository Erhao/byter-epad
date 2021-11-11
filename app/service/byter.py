# -*- coding: utf-8 -*-
from app.db.client import redis_client
from app.utils import prc_now, fmt_dt


def save_cnt(mac, bid, cnt):
    """
    保存cnt到redis
    :param mac:
    :param bid:
    :param cnt:
    :return:
    """
    rds = redis_client()
    now = prc_now()
    hour = fmt_dt(now, "HH")
    now_ymd = fmt_dt(now)
    rkey = f"{bid}__{mac}__{now_ymd}"
    hkey = hour
    print(f"save {rkey} {hkey} {cnt} to redis")
    rds.hset(rkey, hkey, cnt)
