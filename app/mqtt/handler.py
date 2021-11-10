# -*- coding: utf-8 -*-
import json
from app.service.byter import save_cnt


"""
定义topic及其对应处理函数
"""

sub_byter_cnt_topic = "byter/v1.0"


def sub_byter_cnt_topic_handler(client, userdata, msg):
    """
    接收byter上报的cnt并处理
    :return:
    """
    print("Received message '" + str(msg.payload) + "' on topic '"
          + msg.topic + "' with QoS " + str(msg.qos))
    data = json.loads(msg.payload.decode())

    mac = data['mac']
    bid = data['mac']
    cnt = data['cnt']

    # 保存cnt
    save_cnt(mac, bid, cnt)
