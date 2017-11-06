from django.db import models
from django.utils.encoding import smart_text
from django.utils.encoding import python_2_unicode_compatible

import datetime
from django.utils import timezone

class Article(models.Model):
    class Meta():
        db_table = "article"
    article_title = models.CharField(max_length = 200)
    article_text = models.TextField()
    article_date = models.DateTimeField()
    article_likes = models.IntegerField(default = 0)

    def was_published_recently(self):
        return self.article_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'article_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def __str__(self):
        return smart_text(self.article_title)



class Comments(models.Model):
    class Meta():
        db_table = "comments"
    comments_text = models.TextField()
    comments_article = models.ForeignKey(Article)
    def __str__(self):
        return self.comments_text
