# -*- coding:utf-8 -*-
#name:get_weibo_content.py
#time:20130307

'''根据mid批量获取微博文本内容，用于微博文本分析'''

import json
import csv
import time
from weibo import APIClient
import os
import Queue
import threading
import _winreg



def access_client():
    app_key=''
    app_secret=''
    redirect_uri=''
    #写死token
    access_token='2.00PST4KCWVrioD3aee250b49D7w6oB'
    expires_in='1520329130'

    client = APIClient(app_key=app_key, app_secret=app_secret, redirect_uri=redirect_uri)
    client.set_access_token(access_token,expires_in)

    return client


#线程
class ThreadMid(threading.Thread):
    def __init__(self, queue):
      threading.Thread.__init__(self)
      self.queue = queue

    def run(self):
      while True:
        mid=self.queue.get()
        try:
            r= client.statuses.show.get(id=mid)
            result=r['text']
        except Exception,e:
            result=e[0]
        result_list.append(result)
        self.queue.task_done()


#获取当前系统桌面路径
def get_desktop():
    key=_winreg.OpenKey(_winreg.HKEY_CURRENT_USER,\
                          r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders',)
    desktop=_winreg.QueryValueEx(key, "Desktop")[0]
    return desktop


#创建结果文件
def create_csv(result_list):
    desktop=get_desktop()
    f=open(os.path.join(desktop+u'\\微博文本_'+time.strftime('%M%S')+'.csv'),'wb')
    writer=csv.writer(f)    
    for item in result_list:
        try:
            writer.writerow([item.encode('gb2312')])
        except:
            writer.writerow(['writer error'])
    f.close()




def main():
    #传入mid
    mid=raw_input(u'请输入mid:')
    mid=mid.split('\n')

    start=time.time()
    
    global client
    client=access_client()

    global result_list
    result_list=[]
    
    queue=Queue.Queue()

    for i in range(100):
        t=ThreadMid(queue)
        t.setDaemon(True)
        t.start()

    for item in mid:
        queue.put(item)

    queue.join()

    create_csv(result_list)

    end=time.time()
    print "Elapsed Time: %s" % (end- start)



if __name__=='__main__':
    main()
    print 'ok'
    


