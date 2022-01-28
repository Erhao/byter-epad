# -*- coding: utf-8 -*-
import threading

from app.mqtt.client import recv_mqtt_msg
from app.mqtt.handler import sub_byter_cnt_topic, sub_byter_cnt_topic_handler
from app.epaper.epaper import EPaper
from app.statistic.keystoke import KeyStokeStatistic

def run():
    # 接收MQTT消息
    mqtt_thread = threading.Thread(target=recv_mqtt_msg, args=('imac-cli', sub_byter_cnt_topic, sub_byter_cnt_topic_handler))
    mqtt_thread.start()

    # 数据统计
    stat_ins = KeyStokeStatistic()
    stat_ins.start_stat()

    # epaper显示
    # epaper = EPaper()
    # epaper.partial_refresh()


if __name__ == "__main__":
    run()
