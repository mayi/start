# coding: utf-8
import sys
import web
import dbUtil
from settings import render
import simplejson

class Add:
    def GET(self):
        db = dbUtil.DBUtil('lib.db')
        i = web.input()
        db.execute("insert into exes(name, cmd, time, enabled) values (?, ?, ?, ?)", (i.name, i.cmd, i.time, i.enabled))
        maxId = db.selectOne("select max(id) from exes")
        return maxId

class Update:
    def GET(self):
        db = dbUtil.DBUtil('lib.db')
        i = web.input()
        print i.name, i.cmd, i.time, i.enabled
        db.execute("update exes set name = ?, cmd = ?, time = ?, enabled = ? where id = ?", (i.name, i.cmd, i.time, i.enabled, i.id))
        return 'ok'

class UpdateEnabled:
    def GET(self):
        db = dbUtil.DBUtil('lib.db')
        i = web.input()
        print i.enabled
        db.execute("update exes set enabled = ? where id = ?", (i.enabled, i.id))
        return 'ok'

class Delete:
    def GET(self):
        db = dbUtil.DBUtil('lib.db')
        i = web.input()
        db.execute('delete from exes where name = ?', (i.name,))
        return 'ok'