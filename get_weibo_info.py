# -*- coding:utf-8 -*-
#name:get_weibo_info
#time:20130307
'''根据mid批量获取微博文本内容，单线程版本。'''

import json
import csv
import time
from weibo import APIClient
import re
import os


def main():

    access_token=''
    expires_in=''
    app_key=''
    app_secret=''
    redirect_uri=''
    result_list=[]

    client = APIClient(app_key=app_key, app_secret=app_secret, redirect_uri=redirect_uri)
    client.set_access_token(access_token,expires_in)

    mid=raw_input(u'请输入mid:')
    mid=mid.split('\n')
    for item in mid:
        try:
            r= client.statuses.show.get(id=item)
            result=r['text']
        except Exception,e:
            result=e[0]
        result_list.append(result)

    f=open(os.path.join(os.getcwd(),'\\result_'+time.strftime('%M%S')+'.csv'),'wb')
    writer=csv.writer(f)
    for item in result_list:
        try:
            writer.writerow([item.encode('gb2312')])
        except:
            writer.writerow(['writer error'])
        



if __name__=='__main__':
    main()
    print 'ok'


