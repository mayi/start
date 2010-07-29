# coding: utf-8

import sys
import web
import url

sys.path.append('./controllers')
urls = url.urls

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
