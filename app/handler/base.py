#!/usr/bin/env python
#-*- coding:utf8 -*-
# Power by null 2018-02-07 20:05:29
import json
import time
import tornado.web
import traceback
from tornado.web import HTTPError
from app.config import config
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
import os
from datetime import datetime

def static_url(name):
    return os.path.join("/", config.static, name)

def strtime(value):
    value = int(value)
    dt = datetime.fromtimestamp(value)
    return "{}年{}月{}日".format(dt.year, dt.month, dt.day) 

class JinJa2():
    _instance = None
    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(JinJa2, cls).__new__(cls, *args, **kw)
            cls._instance.init()
        return cls._instance
    
    def init(self):
        template_dirs = [config.template_path]
        self.env = Environment(loader=FileSystemLoader(template_dirs))
        self.env.globals['static_url'] = static_url
        self.env.filters['strtime'] = strtime
    
    def render_html(self, template_name, context_dict):
        try:
            template = self.env.get_template(template_name)
        except TemplateNotFound:
            raise TemplateNotFound(template_name)
        content = template.render(context_dict)
        return content    
        

class BaseHandler(tornado.web.RequestHandler):

    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)
        self.mongodb = config.mongodb
        self.jinja = JinJa2()

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
    
    def render_html(self, template_name, context_dict=None, **kw):
        if not context_dict:
            context_dict = {}
        context_dict.update(kw)
        content = self.jinja.render_html(template_name, context_dict)
        self.write(content)

