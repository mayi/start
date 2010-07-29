#-*- encoding:utf-8 -*-
import os
import threading
import time
from subprocess import Popen, PIPE

class StartThread(threading.Thread):
    def __init__(self, cmd, time):
        threading.Thread.__init__(self)
        self.__cmd = cmd
        self.__time = time
        self.p = None

    def run(self):
        if self.__time == '0000-00-00 00:00':
            self.p = Popen(self.__cmd)
            print self.p.pid
        else:
            inputymdhm = (int(self.__time[0:4]), int(self.__time[5:7]), int(self.__time[8:10]), int(self.__time[11:13]), int(self.__time[14:16]))
            print inputymdhm
            while 1:
                t = time.localtime(time.time())
                ymdhm = t[:5]
                if ymdhm > inputymdhm:
                    print 'small'
                    break
                elif ymdhm == inputymdhm:
                    print 'now'
                    self.p = Popen(self.__cmd)
                    print self.p.pid
                    break
                print 'not yet'
                time.sleep(31)

    def returnP(self):
        return self.p

class Starter():
    def __init__(self):
        self.__ps = []

    def start(self, name, cmd, time='0000-00-00 00:00'):
        st = StartThread(cmd, time)
        st.start()
        while st.isAlive():
            continue
        p = {}
        p['name'] = name
        p['process'] = st.returnP()
        self.__ps.append(p)
        print p

    def getPS(self):
        return self.__ps
    
def start(cmd):
    p = Popen(cmd)
    
if __name__ == '__main__':
    start('D:/Program Files/Mozilla Firefox/firefox.exe')
    
