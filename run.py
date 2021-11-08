# -*- coding: utf-8 -*-

from app.mqtt.client import mqtt_cli
from app.mqtt.handler import sub_byter_cnt_topic, sub_byter_cnt_topic_handler

def init_mqtt():
    """

    :return:
    """
    mqtt_cli.connect_mqtt()
    mqtt_cli.subscribe(sub_byter_cnt_topic, sub_byter_cnt_topic_handler)


def run():
    init_mqtt()


if __name__ == "__main__":
    run()
