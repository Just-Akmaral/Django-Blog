from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import smart_text
from datetime import datetime
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from pip._vendor.requests import auth

from tinymce.models import HTMLField
from tinymce import models as tinymce_model
from tinymce.widgets import TinyMCE


class Profile(models.Model):
    class Meta():
        db_table = "profile"

    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Article(models.Model):
    class Meta():
        db_table = "article"

    article_title = models.CharField(default="a nice article", max_length=200)
    article_subheading = models.CharField(default="this is a nice article", max_length=200)
    article_text = HTMLField(verbose_name='Article Content')
    article_date = models.DateTimeField(timezone.now)
    article_likes = models.IntegerField(default=0)
    article_background = models.ImageField(upload_to='img/background/', default='img/background/background.jpg')
    #article_author = models.ForeignKey(Profile)

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


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
