# -*- coding: utf-8 -*-
import redis

r = redis.Redis(host='192.168.0.110', port=6379, password="byterepad", decode_responses=True)
r.set('name', 'runoob')  # 设置 name 对应的值
print(r['name'])
print(r.get('name'))  # 取出键 name 对应的值
print(type(r.get('name')))  # 查看类型