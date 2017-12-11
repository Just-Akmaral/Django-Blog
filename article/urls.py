from django.conf.urls import url, include
from article.models import Article, Comments
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from .models import LikeDislike

app_name = 'article'
urlpatterns = [
    url(r'^$', views.ArticlesView.as_view(), name='articles'),
    url(r'^(?P<pk>[0-9]+)/$', views.ArticleView.as_view(), name='article'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^add_comment/(?P<article_id>[0-9]+)/$', views.add_comment, name='add_comment'),
    url(r'^add_article/$', views.add_article, name='add_article'),
    url(r'^edit_article/(?P<article_id>[0-9]+)/$', views.edit_article, name='edit_article'),
    url(r'^login/$', views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^article/(?P<pk>\d+)/like/$',
        login_required(views.VotesView.as_view(model=Article, vote_type=LikeDislike.LIKE)),
        name='article_like'),
    url(r'^article/(?P<pk>\d+)/dislike/$',
        login_required(views.VotesView.as_view(model=Article, vote_type=LikeDislike.DISLIKE)),
        name='article_dislike'),
    url(r'^comment/(?P<pk>\d+)/like/$',
        login_required(views.VotesView.as_view(model=Comments, vote_type=LikeDislike.LIKE)),
        name='comment_like'),
    url(r'^comment/(?P<pk>\d+)/dislike/$',
        login_required(views.VotesView.as_view(model=Comments, vote_type=LikeDislike.DISLIKE)),
        name='comment_dislike'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
