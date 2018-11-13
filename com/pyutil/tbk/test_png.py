#!/usr/bin/env python
# encoding: utf-8

"""
@author: yx@xy
@license: Apache Licence 
@file: test_png.py
@time: 2018-11-14 1:26
"""
import qrcode

def func():
    pass


class Main():
    def __init__(self):
        pass


if __name__ == '__main__':
    # img = qrcode.make('hello, qrcode')
    # img.save('test.png')
    import pygame
    #pygame初始化
    pygame.init()
    # 待转换文字
    text = u"文字转图片"
    #设置字体和字号
    font = pygame.font.SysFont('Microsoft YaHei', 64)
    #渲染图片，设置背景颜色和字体样式,前面的颜色是字体颜色
    ftext = font.render(text, False, (0, 0, 0),(255, 255, 255))
    #保存图片
    pygame.image.save(ftext, "image/image.jpg")#图片保存地址

    pass