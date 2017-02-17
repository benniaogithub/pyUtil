#-*-coding:utf-8-*- 
__author__ = 'liuqin212173'

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import pynlpir

pynlpir.open()
s = '聊天机器人到底该怎么做呢？'
segments = pynlpir.segment(s)
for segment in segments:
    print segment[0], '\t', segment[1]

pynlpir.close()

pynlpir.open()
s = '怎么才能把电脑里的垃圾文件删除'

key_words = pynlpir.get_key_words(s, weighted=True)
for key_word in key_words:
    print key_word[0], '\t', key_word[1]

pynlpir.close()
