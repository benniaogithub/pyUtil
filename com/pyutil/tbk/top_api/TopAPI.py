#-*-coding:utf-8-*- 
# Time:2018/11/8 23:14

__author__ = 'liuqin212173'
import configparser
import hashlib
import time
import urllib
import requests
import re
import logging
import os
import json
from requests.packages import urllib3
urllib3.disable_warnings()
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
class TopAPI(object):
    def __init__(self,confpath=None):
        self.cf=configparser.ConfigParser()
        if confpath:
            self.confpath = confpath
        else:
            self.confpath = "topApi.conf"
        self.cf.read(self.confpath,encoding="utf8")
        self.logger =self.setLogger(self.cf.get("baseconf","topApilog"))
        self.appkey = self.cf.get("baseconf","appkey")
        self.appSecret = self.cf.get("baseconf","appSecret")
        self.kouss_session = self.cf.get("baseconf","kouss_session")
        self.tklpic = self.cf.get("baseconf","tklpic")
        self.tkltext = self.cf.get("baseconf","tkltext")
        self.p_tkl = r"(<<|《|￥)([A-Za-z0-9]{11,11})(\1)"
        self.p_itemid = self.cf.get("baseconf","p_itemid")
        self.p_pid = "(mm_[0-9]{8,10}_[0-9]{7,10}_[0-9]{7,10})"
        self.p_mcntop = "(https?://(?:m\.)?[A-Za-z]+\.(?:top|cn|com)(?:/s)?/[A-Za-z0-9\.]+)"
        self.p_sclick = "(https://s.click.taobao.com/[A-Za-z0-9]+)"

        #self.m_msg_sucess_c = self.cf.get("baseconf","m_msg_sucess_c")
        self.s = requests.session()

    def set_app(self,appkey,appSecret):
        self.appkey = appkey
        self.appSecret = appSecret
        self.cf.set("baseconf","appkey",appkey)
        self.cf.set("baseconf","appSecret",appSecret)
        self.cf.write(open(self.confpath,'w'))

    def set_kouss_session(self,kouss_session):
        self.kouss_session = kouss_session
        self.cf.set("baseconf","kouss_session",kouss_session)
        self.cf.write(open(self.confpath,'w'))

    def ksort(self,d):
        return [(k, d[k]) for k in sorted(d.keys())]

    def md5(self,s, raw_output=False):
        """Calculates the md5 hash of a given string"""
        res = hashlib.md5(s)
        if raw_output:
            return res.digest()
        return res.hexdigest()

    def setLogger(self,path):
        # 第一步，创建一个logger
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)  # Log等级总开关
        # 第二步，创建一个handler，用于写入日志文件
        rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        if path !="":
            if not os.path.exists(path):
                os.makedirs(path.rsplit("/",1)[0])
            log_path = path
        else:
            log_path = "logs/topApi.log"

        fh = logging.FileHandler(log_path, encoding='utf-8',mode='w+')
        fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
        # 第三步，定义handler的输出格式
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        fh.setFormatter(formatter)
        # 第四步，将logger添加到handler里面
        logger.addHandler(fh)


        # 日志
        logger.debug('this is a logger debug message')
        logger.info('this is a logger info message')
        logger.warning('this is a logger warning message')
        # logger.error('this is a logger error message')
        # logger.critical('this is a logger critical message')
        return logger

    def createSign(self,paramArr):
        sign = self.appSecret
        paramArr=sorted(paramArr.items(), key=lambda d: d[0])
        #paramArr = self.ksort(paramArr)
        #paramArr = dict(paramArr)
        #print(paramArr)
        for k, v in paramArr:
            if k != '' and v != '':
                sign += k + v
        sign += self.appSecret
        #print(sign)
        sign = self.md5(sign).upper()
        return sign

    def createStrParam(self,paramArr):
        strParam = ''
        for k, v in paramArr.items():
            if k != '' and v != '':
                strParam += k + '=' + urllib.quote_plus(v) + '&'
        return strParam

    def create_tkl(self,url,tklpic=None,tkltext=None):
        """
        二合一转淘口令
        :param url:
        :param picurl: 淘口令pic
        :param text:
        :return:
        """
        if(not tklpic):
            tklpic = self.tklpic
        if(not tkltext):
            tkltext =self.tkltext

        param = {"logo":tklpic,"url":urllib.unquote(url).split("&",-1)[0],"text":tkltext,"user_id":"24234234234","ext":"{}"}
        content = self.call_TopApi(param,"taobao.tbk.tpwd.create")
        #print(content)
        match = re.search(self.p_tkl,content)
        tkl = ""
        if match:
            tkl = match.group(2)
        return tkl

    def call_TopApi(self,param,method):
       """
       调官方接口
       :param param:
       :param method:
       :return:
       """
       base_param = {'app_key': self.appkey,
                 'v': '2.0',
                 'sign_method': 'md5',
                 'format': 'json',
                  'method':method,
                  'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                  }
       base_param = dict(base_param,**param)
       sign = self.createSign(base_param)
       base_param["sign"]=sign
       try:
            r=self.s.get('http://gw.api.taobao.com/router/rest', params=base_param)
       except:
           self.logger.error("create tkl error")
           return ""
       self.logger.error("create tkl error")
       return r.content

    def parse_tkl(self,tkl):
        """
        解析淘口令 还原成链接
        :param tkl:
        :return:15 其他问题  16 数据格式不对
        """
        for i in range(3):
            _m_h5_tk =""
            param ={"password":tkl}
            appkey = "12574478"
            c_time =str(int(time.time()*1000))
            s = _m_h5_tk+"&"+c_time+"&"+appkey+"&"+json.dumps(param,sort_keys= False)
            sign = self.md5(s)
            api = "com.taobao.redbull.getpassworddetail"
            v = "1.0"
            url = "https://api.m.taobao.com/h5/com.taobao.redbull.getpassworddetail/1.0/?appKey=12574478&v="+v+"&t="+c_time+ "&sign="+sign+ "&api="+api+"&data=" + urllib.quote(json.dumps(param,sort_keys= False))
            r = self.s.get(url,verify=False)
            _m_h5_tk = r.cookies.get("_m_h5_tk","")
            c = r.cookies
            if _m_h5_tk!="":
                break
        if _m_h5_tk!="":
            _m_h5_tk= _m_h5_tk.split("_",1)[0]
            c_time =str(int(time.time()*1000))
            s = _m_h5_tk+"&"+c_time+"&"+appkey+"&"+json.dumps(param,sort_keys= False)
            sign = self.md5(s)
            newurl = "https://api.m.taobao.com/h5/com.taobao.redbull.getpassworddetail/1.0/?appKey=12574478&v="+v+"&t="+c_time+ "&sign="+sign+ "&api="+api+"&data=" + urllib.quote(json.dumps(param,sort_keys= False))
            content = self.s.get(newurl,cookies=c,verify=False).content
            if content.find("SUCCESS")!=-1:
                try:
                    # print(content)
                    url = json.loads(content,encoding="utf8")["data"]["url"]
                    return(url)
                except:
                    self.logger.error("json dump error")
                    return None
        else:
            self.logger.error("tkl parse null")
            return None

    def kouss_convert(self,item_id,pid):
        """
        :param item_id:
        :param pid:
        :return: 15 该item_id对应宝贝已下架或非淘客宝贝
                  16 json格式转换
                  17 其他
        """
        url = "http://gateway.kouss.com/tbpub/privilegeGet/"
        temp = pid.split("_",3)
        adzone_id= temp [3]
        site_id = temp [2]
        headers = { 'Content-Type': 'application/json; charset=UTF-8'}
        data = {
        'adzone_id':adzone_id ,
        'site_id': site_id,
        'item_id':item_id,
        'session':self.kouss_session
        }

        for i in range(3):
            content = self.s.post(url, headers=headers,data=json.dumps(data, ensure_ascii=False).encode('utf8')).content
            # print(content)
            if content.find("该item_id对应宝贝已下架或非淘客宝贝")!=-1:
                self.logger.info("已经下架:  "+item_id)
                break
                return None
            if content.find("uland.taobao.com")!=-1:
                try:
                    return json.loads(content,encoding="utf8")["result"]["data"]
                except:
                    self.logger.error("json dump error")
                    return None
            time.sleep(i+2)
        return None

    def kouss_long2short(self,url_long):
        """
        错误返回error 正常返回url
        :param url_long:
        :return:
        """
        url = "http://gateway.kouss.com/tbpub/spreadGet"
        headers = { 'Content-Type': 'application/json'}
        data ={'requests':[{"url":url_long}]}

        for i in range(3):
            time.sleep(2)
            content = self.s.post(url, headers=headers,data=json.dumps(data, ensure_ascii=False).encode('utf8')).content
            #print(content)
            if content.find("s.click.taobao.com")!=-1:
                try:
                    return json.loads(content,encoding="utf8")["results"]["tbk_spread"][0]["content"]
                except:
                    self.logger.error("json dump error")
                    return "error"
            elif content.find("请求频率过快")==-1:
                self.logger.error("其他错误")
                return "error"
            time.sleep(i+2)
        logging.info("timeout")
        return "error"

    def sclick_short2long(self,url_short):
        """
        主要是sclick跳转后的uland 但是有可能没有券的跳转后还是sclick 直接跳到id页
        :param url_short:
        :return:
        """

        headers= self.s.get(url_short,verify=False,allow_redirects=False).headers
        url = headers.get("Location","")
        if "tu=" in url:
            url1 = url
            #print(url)
            url = url.split("tu=",1)[1]
            url = urllib.unquote(url)

            headers = {'Accept': 'text/html, application/xhtml+xml, */*',
                        'Referer': url1 ,
                        'Accept-Language': 'zh-CN',
                         'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
                         'Accept-Encoding':'gzip,deflate',
                         'Host': 's.click.taobao.com',
                          'Connection': 'Keep-Alive'}

            headers = self.s.get(url,verify=False,headers=headers,allow_redirects=False).headers
             #print(headers)
            url = headers.get("Location","")
            #print(url)
        return url

    def check_long_pid(self,url_long,pid):
        if "uland.taobao.com" not in url_long:
            return False
        else:
            j_r = self.parse_uland(url_long)
            if j_r:
                pid_t = j_r.get("pid","")
                return pid_t==pid
            else:
                return False

    def check_short_pid(self,url_short,pid):
        url_long = self.sclick_short2long(url_short)
        match = re.search(self.p_pid,url_long)
        if match:
            pid_t = match.group(1)
            return pid_t == pid
        else:
            return self.check_long_pid(url_long,pid)

    def parse_uland(self,url):
        """
        官方h5接口
        :param url:
        :return:错误返回none 正确返回json对象
        """
        api ="https://acs.m.taobao.com/h5/mtop.alimama.union.hsf.coupon.get/1.0/?jsv=2.4.0&appKey=12574478&t=1528968734773&sign=854db05a11347be3faa5b0980718c805&api=mtop.alimama.union.hsf.coupon.get&v=1.0&AntiCreep=true&AntiFlood=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1"
        activityId =""
        headers = { 'ContentType': 'application/json; charset=UTF-8'}
        if "activityId=" in url:
            p_a = r"activityId=(.+?)&"
            matct = re.search(p_a,url)
            if matct:
                activityId =matct.group(1)
            else:
                activityId = url.split("activityId=",1)[0]
        p_e = r"e=(.+?)&"
        matct = re.search(p_e,url)
        if matct:
            e =matct.group(1)
        else:
            e = url.split("e=",1)[0]
        if e !="":
            r = self.s.get(api,headers=headers,verify=False)
            _m_h5_tk = r.cookies.get("_m_h5_tk","")
            c = r.cookies
            if _m_h5_tk!="":
                _m_h5_tk= _m_h5_tk.split("_",1)[0]
                param ={"e":e,"activityId":"","pid":"","src":""}
                appkey = "12574478"
                c_time =str(int(time.time()*1000))
                s = _m_h5_tk+"&"+c_time+"&"+appkey+"&"+json.dumps(param,sort_keys= False)
                sign = self.md5(s)
                newurl = "https://acs.m.taobao.com/h5/mtop.alimama.union.hsf.coupon.get/1.0/?jsv=2.4.0&appKey=12574478&t="+c_time+ "&sign="+sign+ "&api=mtop.alimama.union.hsf.coupon.get&v=1.0&AntiCreep=true&AntiFlood=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data=" + urllib.quote(json.dumps(param,sort_keys= False))
                for i in range(3):
                    content = self.s.get(newurl,headers=headers,cookies=c,verify=False).content
                    if content.find("SUCCESS")!=-1:
                        try:
                            c_s = content.find("{")
                            c_e = content.rfind("}")
                            content = (content[c_s:c_e+1])
                            jr = json.loads(content)["data"]["result"]
                            if activityId !="":
                                # print(activityId)
                                jr["activityId"] = activityId
                            return jr
                        except:
                            self.logger.error("json dump error")
                            return None
        return None

    def itemID_convert(self,item_id,pid,sellerId=None,activityId=None,tklpic=None,tkltext=None):
        match = re.search(self.p_itemid,item_id)
        url_long = ""
        url_short = ""
        tkl = ""
        flag = False
        print(item_id)
        if match:
            for i in range(5):
                j_r = self.kouss_convert(item_id,pid)

                if j_r:
                    url_long = j_r.get("coupon_click_url","")
                    #url_long = urllib.unquote(url_long)
                    #url_long = url_long.decode("utf8").encode("gbk")
                    if self.check_long_pid(url_long,pid):
                        flag = True
                        break
            if flag:
                flag = False
                for i in range(5):
                    if  j_r.get("coupon_info","")=="" and activityId:
                        url_long = url_long+"&activityId="+activityId
                    url_short = self.kouss_long2short(url_long)
                    if url_short !="error":
                        if self.check_short_pid(url_short,pid):
                            flag = True
                            break
                if flag:
                    tkl = self.create_tkl(url_long,tklpic,tkltext)
                    j_r = {'url_long': url_long, 'url_short':url_short, 'tkl' : tkl,"coupon_info":j_r.get("coupon_info","")}
                    return j_r
                else:
                    return None
            else:
                return None
        return None

    def jump_convert(self,url_f,pid,sellerId=None,activityId=None,tklpic=None,tkltext=None):
        match = re.search(self.p_mcntop,url_f)
        if match:
            url_f = match.group(0)
            try:
                j_r = self.jump_extract_itemID(url_f)
            except:
                self.logger.error("jump_extract_itemID")
                return None
            if j_r:
                itemID = j_r.get("itemID","")
                if not sellerId:
                    sellerId = j_r.get("sellerID","")
                if itemID!="":

                    return self.itemID_convert(itemID,pid,sellerId,activityId,tklpic,tkltext)
        return None

    def jump_extract_itemID(self,url):
        """
        通过跳转的方式获取itemID  兜底的
        同时返回sellerID
        :param url:
        :return: json
        """
        itemID = ""
        sellerID = ""
        p_id = r"id=([0-9]{11,12})"

        try:
            content = self.s.get(url,verify=False).content
            if content:
                p_am = r"a\.m\.(?:taobao|tmall)\.com/i([0-9]{11,12})\.htm"
                match = re.search(p_am,content)
                if match:
                    itemID =match.group(1)
                else:
                    match = re.search(p_id,content)
                    if match:
                        itemID =match.group(1)
                    else:
                        p_sclick = r"(https://s.click.taobao.com/t?e=.+?)&)"
                        match = re.search(p_sclick,content)
                        if match:
                            url_t =match.group(1)
                            url_t = self.sclick_short2long(url_t)
                            match = re.search(p_id,url_t)
                            if match:
                                itemID =match.group(1)

                if re.search(self.p_itemid,itemID):
                    p_sellerID_1 = "/i[0-9]/([0-9]{8,12})/"
                    p_sellerID_2 = "\"sellerId\":([0-9]{8,12})"
                    match = re.search(p_sellerID_1,content)
                    if match:
                        sellerID =match.group(1)
                    else:
                        match = re.search(p_sellerID_2,content)
                        if match:
                            sellerID =match.group(1)
            else:
                match = re.search(p_id,url)
                if match:
                    itemID =match.group(1)
            if itemID!="":
                    j_r = {'itemID': itemID, 'sellerID':sellerID}
                    return j_r
        except:
            self.logger.error(url)
            return None
        return None

    def uland_convert(self,url,pid,sellerId=None,activityId=None,tklpic=None,tkltext=None):
        p_uland = "(https?://uland.taobao.com/coupon/edetail\?e=.+)&"
        match = re.search(p_uland,url)
        if match:
            try:
                j_r = self.parse_uland(url)
                if j_r:
                    itemID = j_r.get("item").get("itemId","")
                    activityId = j_r.get("activityId")
                    return self.itemID_convert(itemID,pid,sellerId,activityId,tklpic,tkltext)
            except :

                return None

    def sclick_convert(self,url,pid,sellerId=None,activityId=None,tklpic=None,tkltext=None):
        match = re.search(self.p_sclick,url)
        if match:
            url =match.group(1)
            url = self.sclick_short2long(url)
            if "uland.taobao.com" in url:
                return self.uland_convert(url,pid,sellerId,activityId,tklpic,tkltext)
            else:
                p_id = r"id=([0-9]{11,12})"
                match = re.search(p_id,url)
                if match:
                    itemID =match.group(1)
                    return self.itemID_convert(itemID,pid,sellerId,activityId,tklpic,tkltext)
    def tkl_convert(self,tkl,pid,sellerId=None,activityId=None,tklpic=None,tkltext=None):
        url_long = self.parse_tkl(tkl)
        if url_long:
            return self.uland_convert(url_long,pid,sellerId,activityId,tklpic,tkltext)
        return None
    def msg_convert(self,msg,pid,sellerId=None,activityId=None,tklpic=None,tkltext=None):
        print(msg)
        try:
            if msg == "小蓝单车":
                return """这是小蓝单车10次免费券：
https://gsactivity.diditaxi.com.cn/gulfstream/activity/v2/giftpackage/index?g_channel=d4641b58238e3be424f4edf5b52f9b20
打开链接领取,小蓝和青桔单车通用"""
            elif msg == "vip电影" or msg =="VIP电影":
                return """优酷，爱奇艺，腾讯视频各种VIP资源
请关注微信公众号：野荷塘电影
操作步骤：
      1点击微信下面通信录
      2、点击公众号
      3、点击右上角+号
      4、搜索输入野荷塘电影
      5、进入公众号，点击下方免费电影
      6、点击任何一个电影院或者vip破解
      7、点击左下方《阅读原文》
      8、搜片就可以观看了
说明：该方法包含各平台的资源，与本群无关，只是给大家省钱的一战解决方法，可能不能完全满足你的观影需求，请取消关注该公众号即可。"""

            else:
                p_am = r"a\.m\.(?:taobao|tmall)\.com/i([0-9]{11,12})\.htm"
                #{'url_long': url_long, 'url_short':url_short, 'tkl' : tkl,"coupon_info":j_r.get("coupon_info","")}
                m_msg_sucess_c = """找到如下优惠券:\n优惠券:[coupon_info]\n淘口令:《[tkl]《\n链接:[url_short]\n复制这条消息打开淘宝去下单吧"""
                m_msg_sucess_nc = """优惠券可能被领完了:\n淘口令:<<[tkl]<<\n链接:[url_short]\n复制打开淘宝去看看"""
                m_mot_match = """是我眼神不好@@\n还是你的姿势\n我居然认识这个链接\n请重新再试试"""
                m_s = """===================\n长按 复制 打开淘宝APP\n====================\n"""
                m_e = """\n====================\n"""
                m_tishi ="""====================\n黑科技请私聊我\n发送 宝贝链接 可帮你找优惠券\n输入 小蓝单车 领取免费骑行券\n输入 vip电影 获取vip视频资源\n====================\n"""
                match = re.search(p_am,msg)
                j_r = None
                if match:
                    itemID =match.group(1)
                    j_r = self.itemID_convert(itemID,pid,sellerId,activityId,tklpic,tkltext)
                else:
                    match = re.search(self.p_mcntop,msg)
                    if match:
                        url = match.group(0)
                        j_r = self.jump_convert(url,pid,sellerId,activityId,tklpic,tkltext)
                    else:
                        p_uland = "(https?://uland.taobao.com/coupon/edetail\?e=.+).*&"

                        match = re.search(p_uland,msg)
                        if match:
                            url = match.group(0)
                            if url[-1]=="&":
                                url = url[:-1]
                            j_r = self.uland_convert(url,pid,sellerId,activityId,tklpic,tkltext)
                        else:
                            match = re.search(self.p_sclick,msg)
                            if match:
                                url =match.group(1)
                                j_r = self.sclick_convert(url,pid,sellerId,activityId,tklpic,tkltext)
                            else:
                                match = re.search(self.p_tkl,msg)
                                tkl = ""
                                if match:
                                    tkl = match.group(2)
                                    j_r = self.tkl_convert(tkl,pid,sellerId,activityId,tklpic,tkltext)
                                else:
                                    p_id = r"id=([0-9]{11,12})"
                                    match = re.search(p_id,msg)
                                    if match:
                                        itemID =match.group(1)
                                        j_r = self.itemID_convert(itemID,pid,sellerId,activityId,tklpic,tkltext)
                                    else:
                                        if "http" in msg:
                                            logging.info("msg not match:\t"+msg)
                                            return m_mot_match
                                        else:
                                            return m_tishi

                if j_r:
                    tkl = j_r.get("tkl","")
                    coupon_info = j_r.get("coupon_info","")
                    url_short = j_r.get("url_short","")
                    if coupon_info!="":
                        return (m_s+m_msg_sucess_c.replace("[coupon_info]",coupon_info).replace("[tkl]",tkl).replace("[url_short]",url_short).replace("[url_short]",url_short)+m_e)
                    else:
                        return (m_s+m_msg_sucess_nc.replace("[tkl]",tkl).replace("[url_short]",url_short).replace("[url_short]",url_short)+m_e)
        except:
            self.logger.error("这条消息导致错误:\t"+msg)
            return None




if __name__ == '__main__':
    topApi = TopAPI("topApi.conf")
    #match = re.search("(《|￥)([A-Za-z0-9]{11,11})(\\1)","￥wgmXbjArQNf￥")
    #print(topApi.msg_convert("https://uland.taobao.com/coupon/edetail?e=khG40LNyGIkGQASttHIRqfFuanQDPJiejfUlmsUajwwq3%2BSV041DRTAfnhP8%2FA6QSwtSNeOOJC5XLmfPQjF6k9jNNzEUa%2FOzu0GMKGP2o%2FRYGDYbRJZX5RemP0hpIIPvjDppvlX%2Bob8NlNJBuapvQ2MDg9t1zp0R8pjV3C9qcwTqNdTFElk%2FO%2FNiVGmDoDTz&traceId=0b084a6515419471013441373e&union_lens=lensId:0b0aff46_0ba4_167033590b0_6e67","mm_113949215_18510805_52353400372"))
    #print(topApi.msg_convert("https://s.click.taobao.com/pfhUHKw","mm_113949215_18510805_52353400372"))
    #print(topApi.msg_convert("https://detail.tmall.com/item.htm?id=563235177000&amp;spm=a1z02.1.2016030118.d2016038.462a782dNq4Mjj&amp;scm=1007.10157.81291.100200300000000&amp;pvid=71daa63c-bb37-44eb-ab5d-f7bf90fb62d0 ","mm_113949215_18510805_52353400372"))
    print(topApi.msg_convert("""【迪咕咪婴儿玻璃奶瓶硅胶套防爆防摔防胀宽口径吸管新生儿宝宝用品】用品】https://m.tb.cn/h.3l6tQrk?sm=c3327c 点击链 点击链接，再选择浏览器咑閞；或復·制这段描述￥6QZBbQYxnPh￥后到淘♂寳♀""","mm_113949215_18510805_52353400372"))
    #topApi.set_app("test","test")

    #print(topApi.create_tkl("https://uland.taobao.com/coupon/edetail?e=CDQYrun7YrYGQASttHIRqZgTqzF36V5%2FStCuuzYMc3Qq3%2BSV041DRTAfnhP8%2FA6QSwtSNeOOJC5XLmfPQjF6k9jNNzEUa%2FOzu0GMKGP2o%2FRYGDYbRJZX5RemP0hpIIPvjDppvlX%2Bob8NlNJBuapvQ2MDg9t1zp0R8pjV3C9qcwQGWE84H4PosnHaPPO%2FCBFu&traceId=0b83e94515420518155078536e&union_lens=lensId:0b156441_0bfe_16709736068_e58f"))
    #print(topApi.kouss_convert("580938731821", "mm_113949215_18510805_52353400372"))
    #print(topApi.sclick_short2long("https://s.click.taobao.com/t?e=m=2&s=HuWTUlwLMD4cQipKwQzePOeEDrYVVa64LKpWJ+in0XLjf2vlNIV67sOpFOpnXmU5jGYPrSmetxHODJzgo6UHQvvC/yvf5W8nfTsOaRfcB68I4ycWtPmdtkyvhzmyLK2kthlFgnqEm3+9gxnBL1ozC/O7W2MmBJq7cSpj5qSCmbA=&pvid=16_36.110.147.198_2404_1541770463684&sc=IweULKw"))
    #print(topApi.kouss_long2short("https://s.click.taobao.com/t?e=m=2&s=HuWTUlwLMD4cQipKwQzePOeEDrYVVa64LKpWJ+in0XLjf2vlNIV67sOpFOpnXmU5jGYPrSmetxHODJzgo6UHQvvC/yvf5W8nfTsOaRfcB68I4ycWtPmdtkyvhzmyLK2kthlFgnqEm3+9gxnBL1ozC/O7W2MmBJq7cSpj5qSCmbA=&pvid=16_36.110.147.198_2404_1541770463684&sc=IweULKw"))
    #print(topApi.parse_uland("https://uland.taobao.com/coupon/edetail?e=3IQAaXOU%2F3MGQASttHIRqQIwF%2FNwx7vQkoVMfrzMHeTjBPIDQHOP1dlCudYpna80J13Ht72Xl%2BZgz7i1xqoGX79fwBwwUiql8uAtEhvV%2BV9ERTUVBheqhcHVq%2Fdxq%2FDATJnbK5InWznd4dRbTb5WN9VqM6BWlz38UtqM5E5JIeUSEnxe%2F%2F4Xviu8ITF%2Fm0u9&traceId=0b01f67a15418525328636111e&union_lens=lensId:0b01e2ce_0c2c_166fd929094_2845&activityId=a139cc95d9c44f1fb97b98a1a4f2f0cf&src=xzrj_xztk"))
    #print(topApi.parse_tkl("￥49X1biKdvgY￥"))
    #print(topApi.itemID_convert("575679384191","mm_113949215_18510805_52353400372"))
    #print(topApi.check_short_pid("https://s.click.taobao.com/t?e=m=2&s=HuWTUlwLMD4cQipKwQzePOeEDrYVVa64LKpWJ+in0XLjf2vlNIV67sOpFOpnXmU5jGYPrSmetxHODJzgo6UHQvvC/yvf5W8nfTsOaRfcB68I4ycWtPmdtkyvhzmyLK2kthlFgnqEm3+9gxnBL1ozC/O7W2MmBJq7cSpj5qSCmbA=&pvid=16_36.110.147.198_2404_1541770463684&sc=IweULKw","mm_113949215_16760529_62002931"))
    #print(topApi.check_short_pid("https://s.click.taobao.com/XJgcEKw","mm_113949215_16760529_62002931") )
    #print(topApi.jump_extract_itemID("http://m.rijni.top/h.3k5S6Uv"))
    #print(topApi.jump_convert("http://m.rijni.top/h.3k5S6Uv","mm_113949215_18510805_52353400372"))
    #print(topApi.sclick_convert(""))
    #print(topApi.sclick_convert("https://s.click.taobao.com/pfhUHKw","mm_113949215_18510805_52353400372"))
    #print(topApi.uland_convert("https://uland.taobao.com/coupon/edetail?e=3IQAaXOU%2F3MGQASttHIRqQIwF%2FNwx7vQkoVMfrzMHeTjBPIDQHOP1dlCudYpna80J13Ht72Xl%2BZgz7i1xqoGX79fwBwwUiql8uAtEhvV%2BV9ERTUVBheqhcHVq%2Fdxq%2FDATJnbK5InWznd4dRbTb5WN9VqM6BWlz38UtqM5E5JIeUSEnxe%2F%2F4Xviu8ITF%2Fm0u9&traceId=0b01f67a15418525328636111e&union_lens=lensId:0b01e2ce_0c2c_166fd929094_2845&activityId=a139cc95d9c44f1fb97b98a1a4f2f0cf&src=xzrj_xztk","mm_113949215_18510805_52353400372"))
    #print(topApi.create_tkl("https://uland.taobao.com/coupon/edetail?e=khG40LNyGIkGQASttHIRqfFuanQDPJiejfUlmsUajwwq3%2BSV041DRTAfnhP8%2FA6QSwtSNeOOJC5XLmfPQjF6k9jNNzEUa%2FOzu0GMKGP2o%2FRYGDYbRJZX5RemP0hpIIPvjDppvlX%2Bob8NlNJBuapvQ2MDg9t1zp0R8pjV3C9qcwTqNdTFElk%2FO%2FNiVGmDoDTz&traceId=0b084a6515419471013441373e&union_lens=lensId:0b0aff46_0ba4_167033590b0_6e67"))