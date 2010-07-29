# coding: utf-8
import os
import web

class UploadImage:
    def POST(self):
        i = web.input()
        f = file('static\\screenshot.png', 'wb')
        f.write(i.file)
        f.close()
