#!/bin/python
import json
import sys
import time

line="[{\"watch_mode\":1,\"end\":690,\"state\":0,\"days\":\"1111100\",\"start\":480},{\"watch_mode\":1,\"end\":990,\"state\":0,\"days\":\"1111100\",\"start\":840},{\"watch_mode\":2,\"end\":1400,\"state\":1,\"days\":\"0100000\",\"start\":1140},{\"watch_mode\":2,\"end\":1320,\"state\":0,\"days\":\"1111100\",\"start\":570},{\"watch_mode\":1,\"end\":990,\"state\":0,\"days\":\"1111100\",\"start\":480},{\"watch_mode\":1,\"end\":990,\"state\":0,\"days\":\"1111100\",\"start\":480},{\"watch_mode\":1,\"end\":990,\"state\":0,\"days\":\"1111100\",\"start\":480},{\"watch_mode\":1,\"end\":990,\"state\":0,\"days\":\"1111100\",\"start\":480},{\"watch_mode\":1,\"end\":990,\"state\":0,\"days\":\"1111100\",\"start\":480},{\"watch_mode\":1,\"end\":990,\"state\":0,\"days\":\"1111100\",\"start\":480},{\"watch_mode\":1,\"end\":990,\"state\":0,\"days\":\"1111100\",\"start\":480},{\"watch_mode\":1,\"end\":990,\"state\":0,\"days\":\"1111100\",\"start\":480},{\"watch_mode\":1,\"end\":990,\"state\":0,\"days\":\"1111100\",\"start\":480},{\"watch_mode\":1,\"end\":990,\"state\":0,\"days\":\"1111100\",\"start\":480},{\"watch_mode\":1,\"end\":990,\"state\":0,\"days\":\"1111100\",\"start\":480}]\t1915972\t1"
line=line.rstrip()
setting,user_id,state = line.split('\t')
if len(setting)>10:
    try:
        jsonarr2 = json.loads(setting.replace('\\n',''))
        for item in jsonarr2:
            newstate = str(item['state'])
            if newstate != "":
                state=newstate
            print '\t'.join(('scene',user_id,'1',item['days'],str(item['start']),str(item['end']),state))
    except:
        pass

