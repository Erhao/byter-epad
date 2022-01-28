# -*- coding: utf-8 -*-
import time
import json
from random import randint
from app.mqtt.client import MQTT
from app.mqtt.handler import sub_byter_cnt_topic



"""
模拟byter上报消息
"""

def mock_pub():
    mqtt = MQTT("mock")
    mqtt.connect_mqtt()

    data = {
        'mac': 'fake_mac',
        'bid': 'fake_bid',
        'cnt': '1'
    }
    while True:
        payload = json.dumps(data)
        mqtt.publish(topic=sub_byter_cnt_topic, payload=payload)

        incr = randint(1, 7)
        data['cnt'] = str(int(data['cnt']) + incr)

        wait_seconds = randint(1, 10)
        time.sleep(wait_seconds)


if __name__ == "__main__":
    mock_pub()