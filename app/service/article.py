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
        ''' 
        @param prev: False 请求上一页，True 请求下一页
        @param last_id: 此页的最前一个和最后一个，如果为空则代表取首页
        '''
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
            id_filter_string = '$lt'
            sort_list = [('_id', -1)]
            if prev:
                id_filter_string = '$gt'
                sort_list = [('_id', 1)]
            articles = await self.mongodb.article.find({'_id':{id_filter_string: obj_id}}).sort(sort_list).to_list(limit) 
            if prev:
                articles = articles[::-1]
        if not articles:
            self.result['result'] = False
            self.result['msg'] = '参数错误'
            return
        last_id = articles[-1]['_id']
        first_id = articles[0]['_id']
        return_list = await multi([self.mongodb.article.find({'_id':{'$gte':first_id}}, {'_id':1}).\
                sort([('_id', 1)]).to_list(1),
            self.mongodb.article.find({'_id':{'$lte':last_id}}, {'_id':1}).sort([('_id', -1)]).to_list(1)])
        pre_v = nex_t = None
        if return_list[0]:
            pre_v = str(return_list[0][0]['_id'])
        if return_list[1]:
            nex_t = str(return_list[1][-1]['_id'])
        self.result['info'] = {'articles': articles, 'prev':pre_v if pre_v else '', 'next':nex_t if nex_t else ''}

