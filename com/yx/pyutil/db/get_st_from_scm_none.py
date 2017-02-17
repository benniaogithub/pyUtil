#encoding=utf8

import sys
import MySQLdb
import re

MYSQL_HOST = "storage.teemo.rds.sogou" 
MYSQL_USER      = "tm_dc"      
MYSQL_PWD       = "x1@)!$TeeMo2"     
MYSQL_DB_NAME = "teemo_store"

MYSQL_HOST_TEST = "10.134.9.184"         
MYSQL_USER_TEST      = "teemo_stroe"            
MYSQL_PWD_TEST       = "Teemo_Store"        
MYSQL_DB_NAME_TEST = "teemo_store"


if __name__ == '__main__':

        groupid = None
        verres = None
        spugroup = None
        db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PWD , MYSQL_DB_NAME, charset="utf8")
        #b = MySQLdb.connect(MYSQL_HOST_TEST, MYSQL_USER_TEST, MYSQL_PWD_TEST , MYSQL_DB_NAME_TEST,charset="utf8")
        sql = "SELECT id,NAME,config FROM t_group WHERE scope = 3 AND TYPE='1' AND NAME LIKE '%手表'"
        cur = db.cursor()
        res = ""
        try:
            cur.execute(sql)
        except:
            print("err!")
        rows = cur.fetchall()

        for row in rows:
            temp = row[1][:-2]
            m = re.match(r"\w+",temp)
            if (m and m.group(0)==temp):
                verres = temp
                groupid = str(row[0])
                spugroup = row[2]
                sql2 = "select id from t_product_sku where spu_id in ("+spugroup+")"
                try:
                    cur.execute(sql2)
                except:
                    print("err!")
                result = cur.fetchall()
                skuids=[]
                for sku in result:
                    skuids.append(str(sku[0]))
                sql3 =	"	SELECT DATE_FORMAT(a.form_date,'%Y%m%d'),b.customer_id, \
                    SUM(CASE WHEN b.sub_type=2 AND in_out=-1 THEN COUNT \
                        WHEN  b.sub_type=1 AND in_out=1 THEN -COUNT \
                        WHEN b.sub_type=3 AND in_out=-1 THEN COUNT \
                        WHEN  b.sub_type=4 AND in_out=1 THEN -COUNT ELSE 0 END) AS day0_sum \
                        FROM t_scm_stock_change a,t_scm_sell_form b WHERE sell_cate=2 AND  a.origin_bill_id=b.bill_id \
                        AND sku_id IN ("+','.join(skuids)+") AND origin_form_type = 2  GROUP BY b.customer_id,a.form_date"
                try:
                    cur.execute(sql3)
                except:
                    print("err!")
                result = cur.fetchall()
                for item in result:
                    print('\t'.join((str(item[0]),verres,str(item[1]),str(item[2]))))
            
        db.commit
        db.close



        
