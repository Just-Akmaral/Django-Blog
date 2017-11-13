from django.conf.urls import url
from . import views

app_name = 'article'
urlpatterns = [
    url(r'^$', views.ArticlesView.as_view(), name='articles'),
    url(r'^(?P<pk>[0-9]+)/$', views.ArticleView.as_view(), name='article'),
    url(r'^addLike/(?P<article_id>[0-9]+)/$', views.addLike, name='addLike'),
    url(r'^add_comment/(?P<article_id>[0-9]+)/$', views.add_comment, name='add_comment'),
]
