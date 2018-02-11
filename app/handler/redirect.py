#!/usr/bin/env python
#-*- coding:utf8 -*-
# Power by null 2018-02-08 11:07:20

from app.handler.base import BaseHandler
from tornado.web import HTTPError
import tornado.web

class RedirectAPI(tornado.web.RequestHandler):
    '''
    重定向handler，不支持带参数的get方法，不支持post
    '''
    async def get(self, action=''):
        if action:
            self.redirect(action)
        else:
            raise HTTPError(500)
