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
                self.render_html("admin/login.html")
        elif action == 'login':
            self.render_html("admin/login.html")
        elif action == 'register':
            self.render_html("admin/register.html")
        elif action == 'logout':
            self.clear_cookie('user_name')
            self.render_html("admin/login.html", hint="退出登陆成功！")
        else:
            raise HTTPError(404)

    async def post(self, action=''):
        if action == 'login':
            user_name = self.get_body_argument('user_name', '')
            user_passwd = self.get_body_argument('user_passwd', '')
            await self.service.post_login(user_name, user_passwd) 
            if not self.service.result['err']:
                self.set_secure_cookie('user_name', user_name)
                self.redirect("/") 
                return
            else:
                self.service.result['info'] = {"user_name":user_name, "user_passwd":user_name}
                self.render_html("admin/login.html", self.service.result)
                return
        elif action == 'register':
            user_name = self.get_body_argument('user_name', '')
            user_passwd = self.get_body_argument('user_passwd', '')
            user_passwd_repeat = self.get_body_argument('user_passwd_repeat', '')
            await self.service.post_register(user_name, user_passwd, user_passwd_repeat)
            if not self.service.result['err']:
                self.render_html("admin/login.html", hint="注册成功，清登陆！") 
            else:
                self.render_html("admin/register.html", self.service.result)
        else:
            raise HTTPError(404)
