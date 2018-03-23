from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import smart_text
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import Sum
from tinymce.models import HTMLField
from tinymce import models as tinymce_model
from tinymce.widgets import TinyMCE

class KeyWords(models.Model):
    class Meta():
        db_table = 'keywords'
    name = models.CharField(max_length=50, unique=True, verbose_name='Теги')

    def __str__(self):
        return self.name


class LikeDislikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0

    def articles(self):
        return self.get_queryset().filter(content_type__model='article').order_by('-articles__pub_date')

    def comments(self):
        return self.get_queryset().filter(content_type__model='comment').order_by('-comments__pub_date')


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Dislike'),
        (LIKE, 'Like')
    )

    vote = models.SmallIntegerField(choices=VOTES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Article(models.Model):
    class Meta():
        db_table = "article"

    article_title = models.CharField(default="a nice article", max_length=200)
    article_subheading = models.CharField(default="this is a nice article", max_length=200)
    article_text = HTMLField(verbose_name='Article Content')
    article_date = models.DateTimeField(timezone.now)
    article_background = models.ImageField(upload_to='img/background/', default='img/background/background.jpg')
    article_author = models.ForeignKey(settings.AUTH_USER_MODEL)
    votes = GenericRelation(LikeDislike, related_query_name='articles')
    keywords = models.ManyToManyField(KeyWords, related_name="keywords", related_query_name="keyword",
                                       verbose_name=u'Теги')

    def __str__(self):
        return smart_text(self.article_title)

    def next(self):
        try:
            return Article.objects.get(pk=self.pk + 1)
        except:
            return None

    def previous(self):
        try:
            return Article.objects.get(pk=self.pk - 1)
        except:
            return None


class Comments(models.Model):
    class Meta():
        db_table = "comments"

    comments_text = models.TextField()
    comments_article = models.ForeignKey(Article)
    comments_date = models.DateTimeField(auto_now=True)
    comments_author = models.ForeignKey(settings.AUTH_USER_MODEL)
    votes = GenericRelation(LikeDislike, related_query_name='comments')

    def __str__(self):
        return self.comments_text
