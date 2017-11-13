from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.http import Http404, HttpResponseRedirect
from django.template.context_processors import csrf
from django.views import generic
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse

from django.views.generic.edit import FormView

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Article, Comments

from .forms import CommentForm


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


class ArticleView(generic.DetailView,FormView):
    model = Article
    template_name = 'article/article.html'
    form_class = CommentForm

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
        article.article_likes += 1
        article.save()
    except ObjectDoesNotExist:
        raise Http404
    return HttpResponseRedirect(reverse('article:article', args=(article.id,)))


def add_comment(request, article_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.comments_article = Article.objects.get(id=article_id)
            new_comment.save()
            return HttpResponseRedirect(reverse('article:article', args=(article_id,)))
    else:
        form = CommentForm(instance = request.comments)
        return render('article/article.html',  {'form': form})
    return render(request, 'article/article.html', {
        'form': form
    })
