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
        if not self.get_current_user():
            raise HTTPError(404)
        article_slug = self.get_query_argument("slug", '') 
        if action == 'add':
            if article_slug:
                await self.service.get_article_info(article_slug)
                self.render_html("article_add.html", self.service.result)
            else:
                self.render_html("article_add.html", self.service.result)
        elif action == 'del':
            await self.service.del_one_article(article_slug)
            if not self.service.result['err']:
                self.redirect("/")
                return
            
            raise HTTPError(500)
        else:
            raise HTTPError(404)

    def get_valid_article_info(self):
        info = self.args_2dict(self.request.body_arguments)
        if isinstance(info["tags"], str):
            info["tags"] = [info["tags"],]
        if isinstance(info["catagory"], str):
            info["catagory"] = [info["catagory"],]
        return info

    async def post(self, action=''):
        await self.get_common()
        if not self.get_current_user():
            raise HTTPError(404)
        if action == 'add':
            article_slug = self.get_query_argument("slug", '')
            post_article_info = self.get_valid_article_info()
            if article_slug:
                await self.service.edit_article(article_slug, post_article_info)
            else:
                await self.service.add_article(post_article_info)
            if not self.service.result['err']:
                self.redirect("/{}".format(post_article_info['slug']))
                return
            self.render_html("article_add.html", self.service.result) 

