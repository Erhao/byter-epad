# -*- coding: utf-8 -*-
import time
import threading
import schedule
import logging

from app.decorator import singleton, wrap_logger
from app.db.client import RedisClient
from app.utils import fmt_dt, prc_before_days, prc_before_hours, prc_before_minuts, prc_now, rds_key_generator
from constants import BID, DATE, MAC


logger = logging.getLogger(__file__)
rds = RedisClient()


@singleton
class KeyStokeStatistic():
    def __init__(self):
        self.rds_cli = rds()
    
    @wrap_logger
    def stat_daily(self, dt=None):
        """
        每天统计
        """
        dt = dt if dt else prc_now()

        stat_dt = prc_before_days(1, base=dt)
        
        key = rds_key_generator(DATE, BID, MAC, stat_dt)
        h_all = self.rds_cli.hgetall(key)
        if not h_all:
            logger.info("data not found")
            return
       
        h_keys = list(h_all.keys())
        first_key = h_keys[0]
        last_key = h_keys[-1]

        first_at = ":".join(first_key.split(":")[1:])
        last_at = ":".join(last_key.split(":")[1:])
        raw = h_all[last_at]
        inc = int(h_all[last_at]) - int(h_all[first_at])

        self.rds_cli.hmset(f"{key}_stat", {'raw': raw, 'inc': inc, 'first_at': first_at, 'last_at': last_at})

    @wrap_logger
    def stat_hourly(self, dt=None):
        """
        每小时统计
        """
        dt = dt if dt else prc_now()

        stat_dt = prc_before_hours(1, base=dt)

        key = rds_key_generator(DATE, BID, MAC, stat_dt)
        h_all = self.rds_cli.hgetall(key)
        if not h_all:
            logger.info("hourly hash data not found")
            return
        
        hour = fmt_dt(stat_dt, "HH")
        target_key_prefix = f"{hour}:"
        target_keys = list(filter(lambda k: k.startswith(target_key_prefix), h_all.keys()))
        if not target_keys:
            logger.info("hourly[target] data not found")

        first_key = target_keys[0]
        last_key = target_keys[-1]
        inc = int(h_all[last_key]) - int(h_all[first_key])
        raw = h_all[last_key]

        self.rds_cli.hmset(f"{key}_stat", {f"raw_1h_{hour}": raw, f"inc_1h_{hour}": inc})

    @wrap_logger
    def stat_per_10_mins(self, dt=None):
        """
        每10分钟统计
        """
        dt = dt if dt else prc_now()

        stat_dt = prc_before_minuts(10, base=dt)

        key = rds_key_generator(DATE, BID, MAC, stat_dt)
        h_all = self.rds_cli.hgetall(key)
        if not h_all:
            logger.info("hourly hash data not found")
            return
        
        hour = fmt_dt(stat_dt, "HH")
        minute = fmt_dt(stat_dt, "mm")
        target_key_prefix = f"{hour}:{minute[:1]}"
        target_keys = list(filter(lambda k: k.startswith(target_key_prefix), h_all.keys()))
        if not target_keys:
            logger.info("hourly[target] data not found")
            return
        
        first_key = target_keys[0]
        last_key = target_keys[-1]
        inc = int(h_all[last_key]) - int(h_all[first_key])
        
        self.rds_cli.hmset(f"{key}_stat", {f"inc_10m_{hour}:{minute}": inc})

    def run_in_thread(self, job):
        job_thread = threading.Thread(target=job)
        job_thread.start()

    def start_stat(self):
        # 每天统计
        schedule.every().day.at('00:00').do(self.run_in_thread, self.stat_daily)

        # 每小时统计
        schedule.every().hour.at(':00').do(self.run_in_thread, self.stat_hourly)

        # 每10分钟统计
        schedule.every().hour.at(':00').do(self.run_in_thread, self.stat_per_10_mins)
        schedule.every().hour.at(':10').do(self.run_in_thread, self.stat_per_10_mins)
        schedule.every().hour.at(':20').do(self.run_in_thread, self.stat_per_10_mins)
        schedule.every().hour.at(':30').do(self.run_in_thread, self.stat_per_10_mins)
        schedule.every().hour.at(':40').do(self.run_in_thread, self.stat_per_10_mins)
        schedule.every().hour.at(':50').do(self.run_in_thread, self.stat_per_10_mins)
        
        while 1:
            schedule.run_pending()
            time.sleep(1)
