from django.forms import Textarea, ModelForm, TextInput, DateInput, DateField, forms, CharField, PasswordInput, \
    EmailField, ImageField, FileField, FileInput
from django.contrib.admin.widgets import AdminDateWidget
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from article.models import Comments, Article, User
from django.core.urlresolvers import reverse
from tinymce.widgets import TinyMCE


class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['comments_text', ]
        widgets = {
            'comments_text': Textarea(attrs={'class': 'form-control','placeholder': 'Add comment...'}),
        }


class PostForm(ModelForm):
    class Meta:
        model = Article
        fields = ['article_title', 'article_subheading','article_text','article_background','tags']
        widgets = {
            'article_title': TextInput(attrs={'class': 'form-control','placeholder': 'Add title...'}),
            'article_subheading': TextInput(attrs={'class': 'form-control','placeholder': 'Add subheading...'}),
            'article_date': AdminDateWidget(attrs={'class': 'form-control','placeholder': 'date'}),
        }
        labels = {
            'article_title': _('Add title...'),
            'article_subheading':_('Add subheading...'),
            'article_text': _('Add text...'),
            'article_background': _('Add background...'),
        }
    article_background = ImageField(label=_('Background'),required=False, \
                                    error_messages ={'invalid':_("Image files only")},\
                                    widget=FileInput)
    article_text = CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Media:
        js = (
            '/static/tinymce/jquery.tinymce.min.js',
            '/static/tinymce/tinymce.min.js',
            '/static/tinymce/tiny_mce_init.js',
        )


class SignUpForm(UserCreationForm):
    first_name = CharField(max_length=30, required=True, help_text='Optional')
    last_name = CharField(max_length=30, required=True, help_text='Optional')
    email = EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username',  'first_name', 'last_name', 'email', 'password1', 'password2', )
