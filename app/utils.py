# -*- coding: utf-8 -*-
import arrow


def fmt_dt(dt, fmt="YYYYMMDD"):
    return dt.format(fmt)


def prc_now():
    return arrow.now()
