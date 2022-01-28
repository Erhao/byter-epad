#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import time
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd3in7
from PIL import Image, ImageDraw, ImageFont

from app.decorator import singleton


logging.basicConfig(level=logging.DEBUG)


"""
3.7inch
    局部刷新时间均在0.3秒左右
    全局刷新3秒
    分辨率: 480*280pixels
    灰度等级: 4 黑色 深灰 浅灰 白色

文档: https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html
ImageDraw方法: https://zhuanlan.zhihu.com/p/59849190
    
    * multiline_text
"""

def draw():
    """

    """
    pass


@singleton
class EPaper():
    def __init__(self) -> None:
        self.epd = epd3in7.EPD()
        # 初始化并清屏
        self.epd.init(0)
        self.epd.Clear(0xFF, 0)
        # 定义字体
        self.font36 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 36)
        self.font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
        self.font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

    def clear(self):
        # 初始化并清屏
        self.epd.init(0)
        self.epd.Clear(0xFF, 0)

    def partial_refresh(self):
        self.epd.init(1)         # 1 Gary mode
        self.epd.Clear(0xFF, 1)
        time_image = Image.new('1', (self.epd.height, self.epd.width), 255)
        time_draw = ImageDraw.Draw(time_image)
        num = 0
        while (True):
            time_draw.rectangle((10, 10, 120, 50), fill = 255)
            time_draw.text((10, 10), time.strftime('%H:%M:%S'), font = self.font24, fill = 0)
            self.epd.display_1Gray(self.epd.getbuffer(time_image))
            num = num + 1

            if(num == 100):
                break


def demo():
    try:
        logging.info("epd3in7 Demo")
        
        epd = epd3in7.EPD()
        logging.info("init and Clear")
        # 初始化并清屏
        epd.init(0)
        epd.Clear(0xFF, 0)
        
        # 定义字体
        font36 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 36)
        font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
        font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
        
        # Drawing on the Horizontal image
        # 水平方向
        logging.info("1.Drawing on the Horizontal image...")
        Himage = Image.new('L', (epd.height, epd.width), 0xFF)  # 0xFF: clear the frame
        draw = ImageDraw.Draw(Himage)

        """
        ImageDraw.Draw.text(xy, text, fill=None, font=None, anchor=None, spacing=0, align="left")
        文本
        
        xy 左上角起始坐标
        text 文本
        fill 颜色
        font 字体
        spaceing 多行文本情况下的行间距
        align 多行文本情况下的水平对齐方式, 可以为"left", "center", "right"
        """
        draw.text((10, 0), 'hello world', font = font24, fill = 0)
        draw.text((10, 20), '3.7inch e-Paper', font = font24, fill = 0)
        
        """
        ImageDraw.Draw.rectangle(xy, fill=None, outline=None, width=0)
        矩形
        
        xy 边界 [(x0, y0), (x1, y1)] or [x0, y0, x1, y1]
        fill 填充颜色
        outline 边框颜色
        width 边框宽度, 单位pixels
        """
        draw.rectangle((10, 110, 154, 146), 'black', 'black')
        draw.text((10, 110), u'微雪电子', font = font36, fill = epd.GRAY1)
        draw.text((10, 150), u'微雪电子', font = font36, fill = epd.GRAY2)
        draw.text((10, 190), u'微雪电子', font = font36, fill = epd.GRAY3)
        draw.text((10, 230), u'微雪电子', font = font36, fill = epd.GRAY4)

        """
        ImageDraw.Draw.line(xy, fill=None, width=0, joint=None)
        线

        xy 点与点之间坐标，[(x0, y0), (x1, y1),...] or [x0, y0, x1, y1,....]
        fill 线条填充颜色
        width 线条宽度，单位 pixels
        joint 线之间的联合类型，如: curve 圆角
        """
        draw.line((20, 50, 70, 100), fill = 0)
        draw.line((70, 50, 20, 100), fill = 0)
        draw.rectangle((20, 50, 70, 100), outline = 0)
        draw.line((165, 50, 165, 100), fill = 0)
        draw.line((140, 75, 190, 75), fill = 0)

        """
        ImageDraw.Draw.arc(xy, fill=None, width=0, joint=None)
        圆弧

        xy 点与点之间坐标, 边界的坐标[(x0, y0), (x1, y1)] or [x0, y0, x1, y1]
        start 起始角度, 单位度. 角度从水平位置右方开始, 顺时针方向为正
        end 结束角度
        fill 线条填充颜色, 'red', (255,0,0), '#FF0000', 125 等ImageColor中的颜色表达方式。
        width 线条宽度, 单位 pixels
        """
        draw.arc((140, 50, 190, 100), 0, 360, fill = 0)
        draw.rectangle((80, 50, 130, 100), fill = 0)

        """
        ImageDraw.Draw.chord(xy, start, end, fill=None, outline=None, width=0)
        圆弧, 起始点与结束点使用直线相连, 中间区域填充 fill 颜色，外部线条使用 outline 颜色

        xy 点与点之间坐标, 边界的坐标[(x0, y0), (x1, y1)] or [x0, y0, x1, y1]
        start 起始角度, 单位度. 角度从水平位置右方开始, 顺时针方向为正
        end 结束角度
        fill 线条填充颜色, 'red', (255,0,0), '#FF0000', 125 等ImageColor中的颜色表达方式。
        outline 边框颜色
        width 线条宽度, 单位 pixels
        """
        draw.chord((200, 50, 250, 100), 0, 360, fill = 0)
        epd.display_4Gray(epd.getbuffer_4Gray(Himage))
        time.sleep(5)
        
        logging.info("2.read 4 Gray bmp file")
        Himage = Image.open(os.path.join(picdir, '3in7_4gray2.bmp'))
        epd.display_4Gray(epd.getbuffer_4Gray(Himage))
        time.sleep(5)
        
        logging.info("3.read bmp file on window")
        Himage2 = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        bmp = Image.open(os.path.join(picdir, '100x100.bmp'))
        Himage2.paste(bmp, (200,50))
        epd.display_4Gray(epd.getbuffer_4Gray(Himage2))
        time.sleep(5)
        
        # Drawing on the Vertical image
        logging.info("4.Drawing on the Vertical image...")
        Limage = Image.new('L', (epd.width, epd.height), 0xFF)  # 0xFF: clear the frame
        draw = ImageDraw.Draw(Limage)
        draw.text((2, 0), 'hello world', font = font18, fill = 0)
        draw.text((2, 20), '3.7inch epd', font = font18, fill = 0)
        draw.rectangle((130, 20, 274, 56), 'black', 'black')
        draw.text((130, 20), u'微雪电子', font = font36, fill = epd.GRAY1)
        draw.text((130, 60), u'微雪电子', font = font36, fill = epd.GRAY2)
        draw.text((130, 100), u'微雪电子', font = font36, fill = epd.GRAY3)
        draw.text((130, 140), u'微雪电子', font = font36, fill = epd.GRAY4)
        draw.line((10, 90, 60, 140), fill = 0)
        draw.line((60, 90, 10, 140), fill = 0)
        draw.rectangle((10, 90, 60, 140), outline = 0)
        draw.line((95, 90, 95, 140), fill = 0)
        draw.line((70, 115, 120, 115), fill = 0)
        draw.arc((70, 90, 120, 140), 0, 360, fill = 0)
        draw.rectangle((10, 150, 60, 200), fill = 0)
        draw.chord((70, 150, 120, 200), 0, 360, fill = 0)
        epd.display_4Gray(epd.getbuffer_4Gray(Limage))
        time.sleep(5)

        # partial update, just 1 Gary mode
        logging.info("5.show time, partial update, just 1 Gary mode")
        epd.init(1)         # 1 Gary mode
        epd.Clear(0xFF, 1)
        time_image = Image.new('1', (epd.height, epd.width), 255)
        time_draw = ImageDraw.Draw(time_image)
        num = 0
        while (True):
            time_draw.rectangle((10, 10, 120, 50), fill = 255)
            time_draw.text((10, 10), time.strftime('%H:%M:%S'), font = font24, fill = 0)
            epd.display_1Gray(epd.getbuffer(time_image))
            
            num = num + 1
            if(num == 20):
                break
                
        logging.info("Clear...")
        epd.init(0)
        epd.Clear(0xFF, 0)
        
        logging.info("Goto Sleep...")
        epd.sleep()
        
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd3in7.epdconfig.module_exit()
        exit()