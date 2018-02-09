#!/usr/bin/env python
#-*- coding:utf8 -*-
# Power by null 2018-02-07 20:05:29
import json
import time
import tornado.web
import traceback
from tornado.web import HTTPError
from app.config import config

class BaseHandler(tornado.web.RequestHandler):

    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)
        self.mongodb = config.mongodb

    def get(self, *args, **kwargs):
        raise HTTPError(404)

    def post(self, *args, **kwargs):
        raise HTTPError(404)

    def prepare(self):
        pass 
        
    def on_finish(self):
        pass
    
    def get_current_user(self):
        return self.get_secure_cookie('user_name')

    def args_2dict(self, args):
        if not args:
            return '-'
        args_dict = {}
        for k, v in args.items():
            if isinstance(v, list) and len(v) == 1:
                args_dict[k] = v[0].decode()
            elif isinstance(v, list) and len(v) == 0:
                args_dict[k] = ''
            else:
                args_dict[k] = v
    
        return args_dict
    
