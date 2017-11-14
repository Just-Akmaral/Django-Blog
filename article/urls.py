from django.conf.urls import url, include
from . import views

app_name = 'article'
urlpatterns = [
    url(r'^$', views.ArticlesView.as_view(), name='articles'),
    url(r'^(?P<pk>[0-9]+)/$', views.ArticleView.as_view(), name='article'),
    url(r'^addLike/(?P<article_id>[0-9]+)/$', views.addLike, name='addLike'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^add_comment/(?P<article_id>[0-9]+)/$', views.add_comment, name='add_comment'),
    url(r'^add_article/$', views.add_article, name='add_article'),
    url(r'^edit_article/(?P<article_id>[0-9]+)/$', views.edit_article, name='edit_article'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
]
