#!/bin/python
import json
import sys
import time

import sys
reload(sys)
sys.setdefaultencoding(
"utf-8"
)

# os.path.dirname(os.path.dirname(os.path.abspath("文件名"))) #表示获取当前文件夹上一层目录
#
# import os
# >>> os.chdir("E:\\PycharmProjects\\odycmdb\\odycmdb")
# >>> os.listdir()
# ['settings.py', 'urls.py', 'wsgi.py', '__init__.py', '__pycache__']
# >>> os.path.abspath("settings.py")
# 'E:\\PycharmProjects\\odycmdb\\odycmdb\\settings.py'
# >>> os.path.dirname(os.path.dirname(os.path.abspath("settings.py")))
# 'E:\\PycharmProjects\\odycmdb'