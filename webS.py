#coding:utf-8

import urllib
import simplejson
import base64
import fileuploader

def getAllExe():
    u = urllib.urlopen("http://10.10.10.175:8080/listjson")
    s = u.read()
    print s
    o = simplejson.JSONDecoder('utf-8').decode(s)
    return o
    
def addExe(name, cmd, time, enabled):
    param = {'name': name, 'cmd': cmd, 'time': time, 'enabled': enabled}
    u = urllib.urlopen("http://10.10.10.175:8080/add?" + urllib.urlencode(param))
    id = u.read()
    return id

def updateExe(id, name, cmd, time, enabled):
    param = {'id': id, 'name': name, 'cmd': cmd, 'time': time, 'enabled': enabled}
    u = urllib.urlopen("http://10.10.10.175:8080/update?" + urllib.urlencode(param))
    ret = u.read()
    return ret

def deleteExe(name):
    param = {'name': name}
    u = urllib.urlopen("http://10.10.10.175:8080/delete?" + urllib.urlencode(param))
    ret = u.read()
    return ret

def uploadImage(f):
    fileuploadMgr = fileuploader.FileUploadMgr("http://10.10.10.175:8080/uploadImage")
    fileuploadMgr.upload_file({'file': f})