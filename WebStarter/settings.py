# coding: utf-8

import web

render = web.template.render('templates/', cache=False)
web.template.Template.globals['static'] = '/static'