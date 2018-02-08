#!/usr/bin/env python
#-*- coding:utf8 -*-
# Power by null 2018-02-07 19:59:24

from tornado import web
from app.handler import *

urls = [
    web.URLSpec(r"(.+)/$", RedirectAPI, name='redirect'),
    web.URLSpec(r"/admin/?(.*)", AdminAPI, name='admin'),
    web.URLSpec(r"/(.*)", IndexAPI, name='index'),
]
