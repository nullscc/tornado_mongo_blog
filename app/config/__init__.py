#!/usr/bin/env python
#-*- coding:utf8 -*-
# Power by null 2018-02-07 20:18:26

import os
import json
import tornado.options
from tornado.options import define, options

define("mode", default="", help="mode", type=str)
tornado.options.parse_command_line()

def load_config(mode):
    """加载配置类"""
    if mode == 'PRODUCTION':
        from .production import ProductionConfig
        return ProductionConfig
    else:
        from .local_dev import DevelopmentConfig
        return DevelopmentConfig

def init_config():
    options_mode = options.mode
    if options_mode:
        mode = options_mode
    else:
        mode = os.environ.get('MODE')
    config = load_config(mode)
    config.mode = mode
    return config

config = init_config()

def load_setting():
    """
    :return:
    """
    settings = dict(
         static_path=os.path.join(os.path.dirname(__file__), "static"),
         template_path=os.path.join(os.path.dirname(__file__), "templates"),
         debug=config.mode != 'PRODUCTION',
         cookie_secret = config.cookie_secret,
     )
    return settings

