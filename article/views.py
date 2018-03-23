from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.edit import FormView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Article, Comments, Profile, LikeDislike, Tags
from .forms import CommentForm, PostForm, AuthenticationForm, SignUpForm
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.views import View
from django.contrib.contenttypes.models import ContentType
import json
import calendar
from django.http import JsonResponse


class VotesView(View):
    model = None
    vote_type = None
    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        try:
            likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id,
                                                  user=request.user)
            if likedislike.vote is not self.vote_type:
                likedislike.vote = self.vote_type
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except LikeDislike.DoesNotExist:
            obj.votes.create(user=request.user, vote=self.vote_type)
            result = True

        return HttpResponse(
            json.dumps({
                "result": result,
                "like_count": obj.votes.likes().count(),
                "dislike_count": obj.votes.dislikes().count(),
                "sum_rating": obj.votes.sum_rating()
            }),
            content_type="application/json"
        )


class ArticlesView(generic.ListView):
    context_object_name = 'articles'
    template_name = 'article/articles.html'
    cal = calendar.calendar(2025,2,1,5)

    def get_queryset(self):
        articles = Article.objects.all()
        paginator = Paginator(articles, 4)
        page = self.request.GET.get('page')
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)
        return articles

    def get_context_data(self, **kwargs):
        context = super(ArticlesView, self).get_context_data(**kwargs)
        context['tags_list'] = Tags.objects.all()
        return context

    def __unicode__(self):
        return self.title


class ArticleView(generic.DetailView, FormView):
    model = Article
    template_name = 'article/article.html'
    form_class = CommentForm

    def get_queryset(self):
        article = Article.objects.filter(article_date__lte=timezone.now())
        return article

    def __unicode__(self):
        return self.title

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        context['comments_list'] = Comments.objects.filter(comments_article_id=self.object)
        # context['keyw_s'] = tags.objects.get(pk=pk)
        # context['articles'] = Article.objects.filter(tags__name__exact=context['keyw_s'])
        # print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
        # print(self)
        # print(self.objects.filter(tags))
        # print(self.tags)
        # context['tags_list'] = tags.objects.filter(id=self.object.tags)
        return context


class AboutView(generic.TemplateView):
    template_name = 'article/about.html'

    def __unicode__(self):
        return self.title


@login_required(login_url='/login/')
def add_article(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_article = form.save(commit=False)
            new_article.article_date = timezone.now()
            new_article.article_background = form.cleaned_data['article_background']
            new_article.article_author = request.user
            new_article.save()
            return HttpResponseRedirect(reverse('article:article', args=(new_article.id,)))
    else:
        form = PostForm()
    return render(request, 'article/edit_article.html', {'form': form, 'tags': tags.objects.all()})


@login_required(login_url='/login/')
def edit_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    author = article.article_author
    if author == request.user:
        if request.method == "POST":
            form = PostForm(request.POST, request.FILES, instance=article)
            if form.is_valid():
                article = form.save(commit=False)
                article.article_date = timezone.now()
                article.save()
                return redirect('article:article', pk=article.id)
        else:
            form = PostForm(instance=article)
        return render(request, 'article/edit_article.html', {'form': form,'tags': tags.objects.all()})
    else:
        return HttpResponseRedirect(reverse('article:articles'))


@login_required(login_url='/login/')
def add_comment(request, article_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.comments_article = Article.objects.get(id=article_id)
            new_comment.comments_author = request.user
            new_comment.save()
            return HttpResponseRedirect(reverse('article:article', args=(article_id,)))
    else:
        form = CommentForm(instance=request.comments)
    return render(request, 'article/article.html', {
        'form': form, 'tags': tags.objects.all()
    })


class LoginView(LoginView):
    template_name = 'article/login.html'
    authentication_form = AuthenticationForm

    def get_success_url(self):
        return reverse('article:articles')


class LogoutView(LogoutView):
    def get_next_page(self):
        return reverse('article:articles')


def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('article:articles'))
    else:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('article:articles')
        else:
            form = SignUpForm()
        return render(request, 'article/signup.html', {'form': form})

def tags(request, pk):
    args = {}

    args['tags'] = Tags.objects.all()
    args['keyw_s'] = Tags.objects.get(pk=pk)
    args['articles'] = Article.objects.filter(tags__name__exact=args['keyw_s'])
    return render(request, 'article/tags.html', args)

def calendar_info(request):
    articles = Article.objects.filter(article_date__lte=timezone.now()).order_by('article_date').values('article_date', 'article_title', 'id')
    articles_list = list(articles)

    data = []
    for article in articles_list:
        data.append([
            '{dt.day}/{dt.month}/{dt.year}'.format(dt=article['article_date']),
            article['article_title'],
            str(article['id']),
            '#0BA1BF'
        ])
    return JsonResponse(data, safe=False)