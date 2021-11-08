# -*- coding: utf-8 -*-

"""
定义topic及其对应处理函数
"""

sub_byter_cnt_topic = "byter/v1.0"


def sub_byter_cnt_topic_handler(client, userdata, payload):
    """
    接收byter上报的cnt并处理
    :return:
    """
    print('-------------handler payload:', payload)


