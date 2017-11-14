from django.forms import Textarea, ModelForm, TextInput, DateInput, DateField, forms, CharField, PasswordInput, \
    EmailField
from django.contrib.admin.widgets import AdminDateWidget
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from article.models import Comments, Article, User


class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['comments_text']
        widgets = {
            'comments_text': Textarea(attrs={'class': 'form-control','placeholder': 'Add comment...'}),
        }


class PostForm(ModelForm):
    class Meta:
        model = Article
        fields = ['article_title', 'article_subheading', 'article_img', 'article_text',]
        widgets = {
            'article_title': TextInput(attrs={'class': 'form-control','placeholder': 'Add title...'}),
            'article_subheading': TextInput(attrs={'class': 'form-control','placeholder': 'Add subheading...'}),
            'article_img ': TextInput(attrs={'class': 'form-control','placeholder': 'Add path to img...'}),
            'article_text': Textarea(attrs={'class': 'form-control','placeholder': 'Add text...'}),
            'article_date': AdminDateWidget(attrs={'class': 'form-control','placeholder': 'date'}),
        }
        labels = {
            'article_title': _('Add title...'),
            'article_subheading':_('Add subheading...'),
            'article_img ': _('Add path to img...'),
            'article_text': _('Add text...'),
        }


class SignUpForm(UserCreationForm):
    first_name = CharField(max_length=30, required=False, help_text='Optional.')
    last_name = CharField(max_length=30, required=False, help_text='Optional.')
    email = EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username',  'first_name', 'last_name', 'email', 'password1', 'password2', )