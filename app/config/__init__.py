#!/usr/bin/env python
#-*- coding:utf8 -*-
# Power by null 2018-02-07 20:18:26

import os
import json
import tornado.options
from tornado.options import define, options
import motor

define("mode", default="", help="mode", type=str)

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
    config.static_path= os.path.join(os.path.dirname(os.path.dirname(__file__)), config.static)
    config.template_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), config.template)
    config.mongodb = motor.motor_tornado.MotorClient(config.mongo_url)[config.mongo_database]
    config.mode = mode
    return config

config = init_config()

def load_setting():
    """
    :return:
    """
    settings = dict(
        static_path = config.static_path,
        debug=config.mode != 'PRODUCTION',
        cookie_secret = config.cookie_secret,
     )
    return settings

