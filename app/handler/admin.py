#!/usr/bin/env python
#-*- coding:utf8 -*-
# Power by null 2018-02-07 21:47:06

from .base import BaseHandler
from app.service import AdminService
from tornado.web import HTTPError

class AdminAPI(BaseHandler):

    def __init__(self, *args, **kw):
        super(AdminAPI, self).__init__(*args, **kw)
        self.service = AdminService()

    async def get(self, action=''):
        if action == '':
            if self.current_user:
                self.redirect("/")
            else:
                self.write('please login')
        elif action == 'logout':
            self.clear_cookie('user_name')
            self.write('logout success')
        else:
            raise HTTPError(404)

    async def post(self, action=''):
        if action == 'login':
            user_name = self.get_body_argument('user_name', '')
            user_passwd = self.get_body_argument('user_passwd', '')
            await self.service.post_login(user_name, user_passwd) 
            if self.service.result['result']:
                self.set_secure_cookie('user_name', user_name)
        elif action == 'register':
            user_name = self.get_body_argument('user_name', '')
            user_passwd = self.get_body_argument('user_passwd', '')
            user_passwd_repeat = self.get_body_argument('user_passwd_repeat', '')
            await self.service.post_register(user_name, user_passwd, user_passwd_repeat)
        else:
            raise HTTPError(404)
        self.write(self.service.result)
