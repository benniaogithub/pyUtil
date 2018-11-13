#!/usr/bin/env python
# encoding: utf-8

"""
@author: yx@xy
@license: Apache Licence 
@file: test.py
@time: 2018-11-13 19:17
"""
import requests
import re
import time
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
def getC():
    headers = {
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    'accept': '*/*',
    'referer': 'https://h5.m.taobao.com/?sprefer=sypc00',
    'authority': 'h5api.m.taobao.com',
    'cookie': 't=cff5759b3198bafb639030a7296d6bff; cna=OOz3EwDBHU8CAS9eVNkZGaaY; thw=cn; _m_h5_tk=4dab06478749cf71bcb31296c169e46f_1534260967070; _m_h5_tk_enc=eb5abdfc8a3e52d0f7982d2ab34eb471; isg=BH9_A4W7GMQHLxzbVJKP32QcDlqleywDp44sWxFMGy51IJ-iGTRjVv02ZvbeeKt-',
    }

    params = (
    ('jsv', '2.4.11'),
    ('appKey', '12574478'),
    ('t', '1534253767277'),
    ('sign', '12c6fac6a03cf98c8f912413feeaeaaf'),
    ('api', 'mtop.alimama.union.hsf.coupon.get'),
    ('v', '1.0'),
    ('type', 'jsonp'),
    ('dataType', 'jsonp'),
    ('callback', 'mtopjsonp2'),

    )
    c = None
    c = requests.get('https://h5api.m.taobao.com/h5/mtop.alimama.union.hsf.coupon.get/1.0/', headers=headers,cookies=c, params=params).cookies
    print(c)
    return(c)


class Main():
    def __init__(self):
        pass


if __name__ == '__main__':

    headers = { 'ContentType': 'application/json; charset=UTF-8'}
    url = r"https://acs.m.taobao.com/h5/mtop.alimama.union.hsf.coupon.get/1.0/?jsv=2.4.0&appKey=12574478&t=1528968734773&sign=854db05a11347be3faa5b0980718c805&api=mtop.alimama.union.hsf.coupon.get&v=1.0&AntiCreep=true&AntiFlood=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1"
    s=requests.session()
    # print(getC())
    #print(s.get("http://pub.alimama.com/common/getUnionPubContextInfo.json").content)
    print(s.cookies.get_dict())#先打印一下，此时一般应该是空的。
    r = s.get(url,headers=headers,verify=False).content
    #r = session.get(url,headers=headers,verify=False)
    print(r)
    c=requests.cookies.RequestsCookieJar()#利用RequestsCookieJar获取
    c.set('cookie-name','cookie-value')
    s.cookies.update(c)
    print(s.cookies.get_dict())
    import requests


    pass


