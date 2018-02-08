#!/usr/bin/env python
#-*- coding:utf8 -*-
# Power by null 2018-02-07 21:47:06

from .base import BaseHandler
from app.service import AdminService
from tornado.web import HTTPError

class AdminAPI(BaseHandler):
    async def get(self, action=''):
        if action == '':
            if self.current_user:
                self.redirect("/")
            else:
                self.write('please login')
        else:
            raise HTTPError(404)

    async def post(self, action=''):
        if action == 'login':
            user_name = self.get_body_argument('user_name', '')
            user_passwd = self.get_body_argument('user_passwd', '')
            admin = AdminService()
            result = await admin.post_login(user_name, user_passwd) 
            if result:
                self.set_secure_cookie('user_name', user_name)
            self.write('ok' if result else 'ng') 
        elif action == 'register':
            user_name = self.get_body_argument('user_name', '')
            user_passwd = self.get_body_argument('user_passwd', '')
            user_passwd_repeat = self.get_body_argument('user_passwd_repeat', '')
            admin = AdminService()
            result = await admin.post_register(user_name, user_passwd, user_passwd_repeat)
            self.write('ok' if result else 'ng') 
        else:
            raise HTTPError(404)
