# coding: utf-8
from math import ceil

from django.shortcuts import render, redirect
from django.core.cache import cache


from post.models import Article, Comment
from .helper import page_cache,record_click,get_top_n_articles

@page_cache(10)
def home(request):
    "自己添加分页"
    count = Article.objects.all().count()
    pages = ceil(count/5)

    page = int(request.GET.get('page',1))
    page = 0 if page < 1 or page >= (pages + 1) else (page - 1)
    start = page * 5
    end = start + 5
    articles = Article.objects.all()[start:end]

    # 增加排行榜
    top5 = get_top_n_articles(5)
    return render(request, 'home.html', {'articles': articles,'page':page,'pages':range(pages),'top5':top5})



@page_cache(10)
def article(request):
    a = 0
    aid = int(request.GET.get('aid', 1))
    article = Article.objects.get(id=aid)
    record_click(aid)
    comments = Comment.objects.filter(aid=aid)
    return render(request, 'article.html', {'article': article, 'comments': comments})


def create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        article = Article.objects.create(title=title, content=content)
        return redirect('/post/article/?aid=%s' % article.id)
    else:
        return render(request, 'create.html')


def editor(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        aid = int(request.POST.get('aid'))

        article = Article.objects.get(id=aid)
        article.title = title
        article.content = content
        article.save()
        return redirect('/post/article/?aid=%s' % article.id)
    else:
        aid = int(request.GET.get('aid', 0))
        article = Article.objects.get(id=aid)
        return render(request, 'editor.html', {'article': article})


def comment(request):
    if request.method == 'POST':
        # form = CommentForm(request.POST)
        name = request.POST.get('name')
        content = request.POST.get('content')
        aid = int(request.POST.get('aid'))

        Comment.objects.create(name=name, content=content, aid=aid)
        return redirect('/post/article/?aid=%s' % aid)
    return redirect('/post/home/')


def search(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        articles = Article.objects.filter(content__contains=keyword)
        return render(request, 'home.html', {'articles': articles})
