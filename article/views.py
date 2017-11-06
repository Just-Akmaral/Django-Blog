from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.utils import timezone

from .models import Article

class IndexView(generic.ListView):
    template_name = 'article/index.html'
    context_object_name = 'latest_article_list'
    def get_queryset(self):
        return Article.objects.filter(article_date__lte=timezone.now()).order_by('-article_date')[:5]

class DetailView(generic.DetailView):
    model = Article
    template_name = 'article/detail.html'
    def get_queryset(self):
        return Article.objects.filter(article_date__lte=timezone.now())
