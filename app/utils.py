# -*- coding: utf-8 -*-
import arrow

from constants import INC_PREFIX, TimeModeFmtMap


def fmt_dt(dt, fmt="YYYYMMDD"):
    return dt.format(fmt)


def prc_now():
    return arrow.now()


def prc_before_months(n, base=arrow.now()):
    """
    base后n天
    """
    return base.shift(months=-n)


def prc_before_days(n, base=arrow.now()):
    """
    base后n天
    """
    return base.shift(days=-n)


def prc_before_hours(n, base=arrow.now()):
    """
    base后n小时
    """
    return base.shift(hours=-n)


def prc_before_minuts(n, base=arrow.now()):
    """
    base后n小时
    """
    return base.shift(minutes=-n)


def rds_key_generator(time_mode, bid, mac, dt=None):
    """
    redis.key生成器
    """
    if time_mode not in TimeModeFmtMap:
        raise Exception(f"time_mode: <{time_mode}> is not supported")

    prefix = f"{bid}_{mac}_"
    dt = dt if dt else prc_now()
    key = TimeModeFmtMap[time_mode](dt)
    return prefix + key


def hash_key_generator(time_mode, is_raw=False, dt=None):
    """
    redis.hash.key生成器
    """
    if time_mode not in TimeModeFmtMap:
        raise Exception(f"time_mode: <{time_mode}> is not supported")

    prefix = "" if is_raw else INC_PREFIX  # is_raw为True则不带前缀
    dt = dt if dt else prc_now()
    key = TimeModeFmtMap[time_mode](dt)
    return prefix + key
