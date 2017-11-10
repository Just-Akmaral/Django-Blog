from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.utils import timezone

from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Article, Comments

class ArticlesView(generic.ListView):
    context_object_name = 'articles'
    template_name = 'article/articles.html'


    def get_queryset(self):
        articles = Article.objects.all()
        # Отбираем первые 10 статей
        paginator = Paginator(articles, 5)
        page = self.request.GET.get('page')
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            articles = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            articles = paginator.page(paginator.num_pages)
        return articles

    # def get_queryset(self):
    #     return Article.objects.filter(article_date__lte=timezone.now()).order_by('-article_date')[:3]


    def __unicode__(self):
        return self.title


class ArticleView(generic.DetailView):
    model = Article
    template_name = 'article/article.html'

    def get_queryset(self):
        return Article.objects.filter(article_date__lte=timezone.now())

    def __unicode__(self):
        return self.title

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        context['comments_list'] = Comments.objects.filter(comments_article_id=self.object)
        return context
