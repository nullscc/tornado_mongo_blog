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

    async def get(self, action=''):
        if action=='' or action=='prev' or action=='next':
            last_id = self.get_query_argument('last', '')
            await self.service.get_articles_by_next_prev(False if action=='next' else True, last_id)
            if not self.service.result['err']:
                res = {'result': self.service.result['err'], 'msg': self.service.result['msg'],
                        'len': len(self.service.result['info']['articles']),
                        'next':self.service.result['info']['next'],
                        'prev':self.service.result['info']['prev']}
                self.write(res)
            else:
                self.write(self.service.result)
        else:
            await self.service.get_article_info(action)
            #if not self.service.result['result']:
            #    raise HTTPError(404)
            self.write(self.service.result)
