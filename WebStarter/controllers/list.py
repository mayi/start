# coding: utf-8
import sys
import web
import dbUtil
from settings import render
import simplejson

class Html:
    def GET(self):
        db = dbUtil.DBUtil('lib.db')
        results = db.select("select * from exes")
        return render.list(results)

class Json:
    def GET(self):
        db = dbUtil.DBUtil('lib.db')
        results = db.select("select * from exes")
        web.header("Content-Type", "application/json; charset=utf-8")
        return simplejson.JSONEncoder().encode(results)