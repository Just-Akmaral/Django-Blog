from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.utils import timezone

from .models import Article, Comments

class ArticlesView(generic.ListView):
    template_name = 'article/articles.html'
    context_object_name = 'latest_article_list'
    def get_queryset(self):
        return Article.objects.filter(article_date__lte=timezone.now()).order_by('-article_date')[:]

class ArticleView(generic.DetailView):
    model = Article
    template_name = 'article/article.html'
    def get_queryset(self):
        return Article.objects.filter(article_date__lte=timezone.now())
    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        context['comments_list'] = Comments.objects.filter(comments_article_id=self.object)
        return context
