#!/usr/bin/env python
#-*- coding:utf8 -*-
# Power by null 2018-02-07 18:28:13

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from app.config import load_setting 

define("port", default=8000, help="run on the given port", type=int)
tornado.options.parse_command_line()

class Application(tornado.web.Application):
    def __init__(self):
        from app.urls import urls
        tornado.web.Application.__init__(self, handlers=urls, **load_setting())

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(Application(), xheaders=True)
    http_server.listen(options.port)
    print("runserver on {}".format(options.port))
    tornado.ioloop.IOLoop.instance().start()
