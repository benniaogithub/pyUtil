#!/usr/bin/env python
# encoding: utf-8

"""
@author: yx@xy
@license: Apache Licence 
@file: test_pinjie.py
@time: 2018-11-14 2:16
"""

from PIL import Image
#convent()和resize() 可对size和mode进行调整

rawimg = Image.open("image/mengqiqi.jpg")
rawimg = rawimg.resize((1176,1176))
print(rawimg.size)

im = Image.open("image/test.png")
print(im.size)
rawimg.paste(im,(60,20))
im = Image.open("image/image.jpg")
print(im.size)

rawimg.paste(im,(600,1000))
print(im.size)
rawimg.show()
