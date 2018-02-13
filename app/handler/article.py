#!/usr/bin/env python
#-*- coding:utf8 -*-
# Power by null 2018-02-09 10:00:56
from .base import BaseHandler
from app.service import ArticleService
from tornado.web import HTTPError
from functools import wraps

class ArticleAPI(BaseHandler):

    def __init__(self, *args, **kw):
        super(ArticleAPI, self).__init__(*args, **kw)
        self.service = ArticleService()

    async def get_common(self):
       common = await self.service.common.get_common()
       self.service.result['catagories'] = common['catagories']
       self.service.result['tags'] = common['tags']

    async def get(self, action=''):
        await self.get_common()
        article_slug = self.get_query_argument("slug", '') 
        if action == 'add':
            if article_slug:
                await self.service.get_article_info(article_slug)
                self.render_html("article_add.html", self.service.result)
            else:
                self.render_html("article_add.html", self.service.result)
        else:
            raise HTTPError(404)

    async def post(self, action=''):
        await self.get_common()
        if action == 'add':
            article_slug = self.get_query_argument("slug", '')
            post_article_info = self.args_2dict(self.request.body_arguments)
            if article_slug:
                await self.service.edit_article(article_slug, post_article_info)
            else:
                await self.service.add_article(post_article_info)
            self.render_html("article_add.html", self.service.result) 

