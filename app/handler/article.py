#!/usr/bin/env python
#-*- coding:utf8 -*-
# Power by null 2018-02-09 10:00:56


from .base import BaseHandler
from app.service import ArticleService
from tornado.web import HTTPError

class ArticleAPI(BaseHandler):

    def __init__(self, *args, **kw):
        super(ArticleAPI, self).__init__(*args, **kw)
        self.service = ArticleService()

    async def get(self, action=''):
        article_slug = self.get_query_argument("slug", '') 
        if action == 'add':
            if article_slug:
                await self.service.get_article_info(article_slug)
                self.write(self.service.result)
            else:
                self.write("add article page")
        else:
            raise HTTPError(404)

    async def post(self, action=''):
        if action == 'add':
            article_slug = self.get_query_argument("slug", '')
            post_article_info = self.args_2dict(self.request.body_arguments)
            if article_slug:
                await self.service.edit_article(article_slug, post_article_info)
            else:
                await self.service.add_article(post_article_info)
            self.write(self.service.result) 

        
        
                 
            
