# -*- coding: utf-8 -*-

from app.mqtt.client import recv_mqtt_msg
from app.mqtt.handler import sub_byter_cnt_topic, sub_byter_cnt_topic_handler


def run():
    recv_mqtt_msg('imac-cli', sub_byter_cnt_topic, sub_byter_cnt_topic_handler)


if __name__ == "__main__":
    run()
