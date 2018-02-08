#!/usr/bin/env python
#-*- coding:utf8 -*-
# Power by null 2018-02-08 17:41:38
from app.config import config

class BaseService():
    def __init__(self):
        self.mongodb = config.mongodb

        
