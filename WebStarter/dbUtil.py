#-*- encoding:utf8 -*-
import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class DBUtil():
    def __init__(self, dbPath=None):
        if dbPath is not None:
            self.conn = sqlite3.connect(dbPath)
            self.conn.row_factory = dict_factory#sqlite3.Row
        else:
            raise Error

    def execute(self, sql=None, obj=None):
        if sql is not None:
            try:
                c = self.conn.cursor()
                if obj is None:
                    c.execute(sql)
                else:
                    c.execute(sql, obj)
                self.conn.commit()
                c.close()
            except:
                self.conn.rollback()
                c.close()
                raise

    def select(self, sql=None, obj=None):
        if sql is not None:
            c = self.conn.cursor()
            if obj is None:
                c.execute(sql)
            else:
                c.execute(sql, obj)
            results = []
            for row in c:
                results.append(row)
            c.close()
            return results

    def selectOne(self, sql=None, obj=None):
        if sql is not None:
            c = self.conn.cursor()
            if obj is None:
                c.execute(sql)
            else:
                c.execute(sql, obj)
            results = []
            for row in c:
                results.append(row)
            c.close()
            return results[0]


