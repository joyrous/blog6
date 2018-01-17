from django.core.cache import cache
from redis import Redis

from post.models import Article
# 添加全局的redis
rds = Redis('127.0.0.1',6379,db=9)

def page_cache(times):
    def wrap1(view_func):
        # 缓存页面
        def wrap2(requset,*args,**kwargs):
            key = "zhaoHHPAGES-%s" % requset.get_full_path()
            # 页面直接缓存
            response = cache.get(key)
            if response is None:
                response = view_func(requset,*args,**kwargs)
                cache.set(key,response,times)
                print("DB")
            print("cache")
            return response
        return wrap2
    return wrap1

def record_click(article_id,num=1):
    #记录文章点击
    rds.zincrby("article_click",article_id,num)

def get_top_n_articles(num):
    # 结果是列表，然后每个元素是元祖，
    article_clicks = rds.zrevrange("article_click",0,num,withscores=True)
    article_clicks = [[int(aid),int(clk)] for aid,clk in article_clicks]

    aid_list = [aid for aid, _ in article_clicks]
    article = Article.objects.in_bulk(aid_list) #批量查询，无序的

    for data in article_clicks:
        aid = data[0]
        data[0] = article[aid] #找到最热的文章对象（有序的）

    return article_clicks

