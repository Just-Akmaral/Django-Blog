from django.contrib import admin
from article.models import Article, Comments, KeyWords


class ArticleAdmin(admin.ModelAdmin):
    fields = ['article_title', 'article_subheading','article_text', 'article_date', 'article_background','keywords']
    list_display = ('article_title', 'article_date')
    list_filter = ['article_date']
    search_fields = ['article_title']

    class Media:
        js = (
            '/static/tinymce/jquery.tinymce.min.js',
            '/static/tinymce/tinymce.min.js',
            '/static/tinymce/tiny_mce_init.js',
        )

class KeywordsAdmin(admin.ModelAdmin):
    fields = ['name']

admin.site.register(Article, ArticleAdmin)
admin.site.register(KeyWords, KeywordsAdmin)

