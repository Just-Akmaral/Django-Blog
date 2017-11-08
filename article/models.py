from django.db import models
from django.utils.encoding import smart_text
from django.utils.encoding import python_2_unicode_compatible

import datetime
from django.utils import timezone

class Article(models.Model):
    class Meta():
        db_table = "article"
    article_title = models.CharField(max_length = 200)
    article_subheading =  models.CharField(max_length = 200)
    article_img =  models.CharField(max_length = 200)
    article_text = models.TextField()
    article_date = models.DateTimeField()
    article_likes = models.IntegerField(default = 0)
    def __str__(self):
        return smart_text(self.article_title)



class Comments(models.Model):
    class Meta():
        db_table = "comments"
    comments_text = models.TextField()
    comments_article = models.ForeignKey(Article)
    def __str__(self):
        return self.comments_text
