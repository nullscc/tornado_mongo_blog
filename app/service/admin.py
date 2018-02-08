#!/usr/bin/env python
#-*- coding:utf8 -*-
# Power by null 2018-02-07 21:56:20

def post_login(user_name, user_passwd):
    if user_name == 'admin' and user_passwd == '123456':
        return True
    return False
def post_register(user_name, user_passwd, user_passwd_repeat):
    if user_name == 'admin' and user_passwd == '123456' and user_passwd == user_passwd_repeat:
        return True 
    return False
