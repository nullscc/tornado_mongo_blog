#!/usr/bin/env python
#-*- coding:utf8 -*-
# Power by null 2018-02-09 10:06:22
from .base import BaseService
import pymongo
from bson import ObjectId
from tornado.gen import multi

class ArticleService(BaseService):

    async def get_article_info(self, slug):
        info = await self.mongodb.article.find_one({"slug": slug}, {'_id':0})
        if not info:
            self.result['result'] = False
            self.result['msg'] = 'article for slug:{} not found!'.format(slug)
        self.result['info'] = info
    
    async def add_article(self, article_info):
        try:
            await self.mongodb.article.insert(article_info)
        except pymongo.errors.DuplicateKeyError:
            self.result['result'] = False
            self.result['msg'] = '不能添加重复的文章链接'

    async def edit_article(self, slug, article_info):
        original_doc = await self.mongodb.article.find_one_and_replace({"slug": slug}, article_info)
        if not original_doc:
            self.result['result'] = False
            self.result['msg'] = '要编辑的文章不存在'

    async def get_articles_by_next_prev(self, prev=False, last_id=''):
        limit = 20
        if not last_id:
            articles = await self.mongodb.article.find({}).sort([('_id', -1)]).to_list(limit)
        else:
            obj_id = None
            try:
                obj_id = ObjectId(last_id) 
            except:
                self.result['result'] = False
                self.result['msg'] = '参数错误'
                return
            articles = await self.mongodb.article.find({'_id':{'$lt':obj_id}}).sort([('_id', -1)]).to_list(limit) 
        if not articles:
            self.result['result'] = False
            self.result['msg'] = '参数错误'
            return
        last_id = articles[-1]['_id']
        first_id = articles[0]['_id'] 
        
        pre_v, nex_t = await multi([self.mongodb.article.find_one({'_id':{'$gt':first_id}}, {'_id':1}),
            self.mongodb.article.find_one({'_id':{'$lt':first_id}}, {'_id':1})])
        self.result['info'] = {'last': str(articles[-1]['_id']), 'articles': articles,
                'has_prev':True if pre_v else False, 'has_next':True if nex_t else False}

