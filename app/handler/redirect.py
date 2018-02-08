#!/usr/bin/env python
#-*- coding:utf8 -*-
# Power by null 2018-02-08 11:07:20

from app.handler.base import BaseHandler
from tornado.web import HTTPError

class RedirectAPI(BaseHandler):

    async def get(self, action=''):
        if action:
            self.redirect(action)
        else:
            raise HTTPError(500)
