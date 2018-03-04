#!/usr/bin/env python
#-*- coding:utf8 -*-
# Power by null 2018-02-07 20:01:48
from app.handler.base import BaseHandler
from tornado.web import HTTPError
from app.service import ArticleService

class IndexAPI(BaseHandler):
    def __init__(self, *args, **kw):
        super(IndexAPI, self).__init__(*args, **kw)
        self.service = ArticleService()

    async def get_common(self):
       common = await self.service.common.get_common()
       self.service.result['catagories'] = common['catagories']
       self.service.result['tags'] = common['tags']

    async def get(self, action=''):
        await self.get_common()
        if action=='' or action=='prev' or action=='next':
            last_id = self.get_query_argument('last', '')
            await self.service.get_articles_by_next_prev(False if action=='next' else True, last_id)
            if not self.service.result['err']:
                self.render_html("index.html", self.service.result)
        elif action=='tags' or action=='catagories' or action=='drafts':
            last_id = self.get_query_argument('last', '')
            prev = True if int(self.get_query_argument('prev', 0)) else False
            name = self.get_query_argument('name', '')
            if not self.service.result['err']:
                if action=='tags':
                    await self.service.get_articles_by_next_prev(prev, last_id, tag_name=name)
                    self.render_html("index.html", self.service.result, tag=name)
                elif action=='catagories':
                    await self.service.get_articles_by_next_prev(prev, last_id, catagory_name=name)
                    self.render_html("index.html", self.service.result, catagory=name)
                elif action=='drafts':
                    await self.service.get_articles_by_next_prev(prev, last_id, status=1)
                    self.render_html("index.html", self.service.result, status=1)
        else:
            await self.service.get_article_info(action, True)
            if self.service.result['err']:
                raise HTTPError(404)
            self.render_html("single_article.html", self.service.result)
