from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import smart_text
from django.utils.encoding import python_2_unicode_compatible
from datetime import datetime
import datetime
from django.utils import timezone
from django.contrib.auth.models import User


class Article(models.Model):
    class Meta():
        db_table = "article"

    article_title = models.CharField(max_length=200)
    article_subheading = models.CharField(max_length=200)
    article_img = models.CharField(max_length=200, default="/img/post-bg-1.jpg")
    article_text = models.TextField()
    article_date = models.DateTimeField(default=datetime.date.today)
    article_likes = models.IntegerField(default=0)

    def __str__(self):
        return smart_text(self.article_title)


class Comments(models.Model):
    class Meta():
        db_table = "comments"

    comments_text = models.TextField()
    comments_article = models.ForeignKey(Article)

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