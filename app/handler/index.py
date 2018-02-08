#!/usr/bin/env python
#-*- coding:utf8 -*-
# Power by null 2018-02-07 20:01:48
from app.handler.base import BaseHandler
from tornado.web import HTTPError

class IndexAPI(BaseHandler):

    async def get(self, action=''):
        if action == '':
            self.write('home page')
        elif action == 'hello':
            self.write("hello tornado!!!")
        else:
            raise HTTPError(404)
