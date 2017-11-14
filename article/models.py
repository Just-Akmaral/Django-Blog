from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import smart_text
from django.utils.encoding import python_2_unicode_compatible
from datetime import datetime
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime
# from tinymce.models import HTMLField
# from tinymce import models as tinymce_model

import tinymce


class Article(models.Model):
    class Meta():
        db_table = "article"

    article_title = models.CharField(default="a nice article", max_length=200)
    article_subheading = models.CharField(default="this is a nice article", max_length=200)
    article_img = models.CharField(max_length=200, default="https://images.unsplash.com/photo-1507834251994-9191f78e15ac?auto=format&fit=crop&w=1936&q=60&ixid=dW5zcGxhc2guY29tOzs7Ozs%3D")
    article_text = models.TextField(default="Nice text!")
    article_date = models.DateTimeField(timezone.now)
    article_likes = models.IntegerField(default=0)
    # article_content = HTMLField()

    def __str__(self):
        return smart_text(self.article_title)


class Comments(models.Model):
    class Meta():
        db_table = "comments"

    comments_text = models.TextField()
    comments_article = models.ForeignKey(Article)
    comments_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comments_text


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     location = models.CharField(max_length=30, blank=True)
#
#
# @receiver(post_save, sender=User)
# def update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()