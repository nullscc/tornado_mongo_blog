#!/usr/bin/env python
#-*- coding:utf8 -*-
# Power by null 2018-02-07 21:56:20
from .base import BaseService
from hashlib import md5

class AdminService(BaseService):
    async def post_login(self, user_name, user_passwd):
        password_md5 = md5(user_passwd.encode('utf8')).hexdigest()
        user_record = await self.mongodb.user.find_one({'name': user_name})
        if user_record and user_record['passwd'] == password_md5:
            return True
        return False
    async def post_register(self, user_name, user_passwd, user_passwd_repeat):
        if not self.check_passwd_valid(user_passwd, user_passwd_repeat):
            return False 
        if await self.check_has_register():
            return False
        password_md5 = md5(user_passwd.encode('utf8')).hexdigest()
        self.mongodb.user.insert_one({'name': user_name, 'passwd': password_md5})
        return True

    @staticmethod
    def check_passwd_valid(passwd, passwd_repeat):
        if passwd == passwd_repeat:
            return True
        return False
        
    async def check_has_register(self):
        r = await self.mongodb.user.find_one() 
        if r:
            return True
        return False

