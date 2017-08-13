# coding: utf-8

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import sys


from tornado.options import define, options

from com.listen.tushare.web.dbservice.DbService import DbService


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        dbService = DbService()
        self.render('index_easyui.html')

