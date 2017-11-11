from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Article, Comments

class ArticlesView(generic.ListView):
    context_object_name = 'articles'
    template_name = 'article/articles.html'

    def get_queryset(self):
        articles = Article.objects.all()
        paginator = Paginator(articles, 3)
        page = self.request.GET.get('page')
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)
        return articles

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


def addLike(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    try:
    #    article = Article.objects.get(pk=article_id)
        article.article_likes += 1
        article.save()
    except ObjectDoesNotExist:
        raise Http404
    return HttpResponseRedirect(reverse('article:article', args=(article.id,)))
