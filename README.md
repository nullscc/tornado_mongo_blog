# tornado_mongo_blog
使用tonado与mongo开发的个人blog

# 说明
1. 第一个版本尽量不使用redis与js
2. 登陆完全使用浏览器secure cookie

# 下版本待优化:
1. markdown渲染的文本使用redis缓存
2. 利用redis实现服务器session

# 建立索引
1. `db.article.ensureIndex({"slug":1}, {"unique": true})`
