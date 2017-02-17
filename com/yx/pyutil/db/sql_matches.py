#-*-coding:utf-8-*- 
__author__ = 'liuqin212173'
if __name__ == '__main__':

        # # read = open("f://func_act.data")
        # read = open("f://camera_effect")
        # line=read.readline()
        # outline = ""
        # while line:
        #       temp = line.split()
        #       size = len(temp)
        #
        #       for i in range(1,size):
        #
        #           if int(temp[i])>0:
        #               outline += "camera_effect_cnts\t"+str(i-1)+"\t"+temp[0]+"\t"+"M1"+"\t"+temp[i]+"\t"+"0"+"\t"+"0"+"\n"
        #       line=read.readline()#如果没有这行会造成死循环
        outline=""
        for i in range(20161114,20161123):
            outline += '''sh /search/teemo-dc-dataanalysis/spark/sqlSelectExecutor.sh -s"
add jar /search/teemo-dc-dataanalysis/lib/teemo-dc-udf-jar-with-dependencies.jar;
create temporary function snToModelT1 as 'com.test.hive.udf.UDFSNToModelT1';

INSERT OVERWRITE TABLE tm.tm_baby_event_distemp partition(cdate='''+str(i)+''')
select settingtype,id,user_id,platform,sum(shezhipv),sum(shanchupv),sum(xiazaipv) from
	(select settingtype,id,user_id,platform,count(case when action=1 then user_id end) as shezhipv,count(case when action=2 then user_id end) as shanchupv,count(case when action=3 then user_id end) as xiazaipv from
		(select cdate,extra['settingtype'] as settingtype,user_id,platform,extra['id'] as id,extra['event'] as action
		from teemo_baby_active  where cdate='''+str(i)+'''  and action='displaysetting'
		)a
	group by cdate,settingtype,id,platform,user_id
	union all
 	select settingtype,id,user_id,platform,shezhipv,shanchupv,xiazaipv from tm.tm_baby_event_phototemp
	where cdate='''+str(i)+'''  and (settingtype='camera_effect_cnts' or settingtype='sticker_detail_cnt')
	union all
	select settingtype,id,user_id,platform,shezhipv,shanchupv,xiazaipv from tm.tm_baby_event_distemp
	where cdate='''+str(i-1)+'''
	)b
group by settingtype,id,platform,user_id
"'''+"\n"



#                         outline += '''sh /search/teemo-dc-dataanalysis/spark/sqlSelectExecutor.sh -s"
# add jar /search/teemo-dc-dataanalysis/lib/teemo-dc-udf-jar-with-dependencies.jar;
# create temporary function snToModelT1 as 'com.test.hive.udf.UDFSNToModelT1';
#
# INSERT OVERWRITE TABLE tm.tm_baby_event_distemp partition(cdate='''+str(i)+''')
# select settingtype,id,user_id,platform,sum(shezhipv),sum(shanchupv),sum(xiazaipv) from
# 	(select settingtype,id,user_id,platform,count(case when action=1 then user_id end) as shezhipv,count(case when action=2 then user_id end) as shanchupv,count(case when action=3 then user_id end) as xiazaipv from
# 		(select cdate,extra['settingtype'] as settingtype,user_id,platform,extra['id'] as id,extra['event'] as action
# 		from teemo_baby_active  where cdate='''+str(i)+'''  and action='displaysetting'
# 		)a
# 	group by cdate,settingtype,id,platform,user_id
# 	union all
# 	select settingtype,id,user_id,platform,shezhipv,shanchupv,xiazaipv from tm.tm_baby_event_distemp
# 	where cdate='''+str(i)+'''  and (settingtype='camera_effect_cnts' or settingtype='sticker_detail_cnt')
# 	union all
# 	select settingtype,id,user_id,platform,shezhipv,shanchupv,xiazaipv from tm.tm_baby_event_distemp
# 	where cdate='''+str(i-1)+''' and (settingtype='camera_effect_cnts' or settingtype='sticker_detail_cnt')
# 	)b
# group by settingtype,id,platform,user_id
# "'''+"\n"


#                 outline +='''HADSRC=/user/teemo/log/storage/sogou/upd/upd-x1-tcplog/201611/'''+str(i)+'''
# HADRES=/user/teemo/tmp/babyrings/wh_tcplog
# hadoop fs -rm -r $HADRES
# hadoop jar /search/teemo-dc-dataanalysis/warehouse/teemo-dc-etl-1.0.0-jar-with-dependencies.jar com.sogou.tcplog_tm.TcpLogTm $HADSRC $HADRES
# /usr/lib/hive/bin/hive -e "load data inpath '$HADRES/photo-*' overwrite into table tm.tm_baby_event_phototemp partition (cdate='''+str(i)+''');"'''+"\n"
#
        write = open("f://sql","w")
        write.write(outline)