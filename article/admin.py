from django.contrib import admin
from article.models import Article, Comments


# class ArticleInline(admin.TabularInline):
#     model = Comments
#     extra = 2


class ArticleAdmin(admin.ModelAdmin):
    fields = ['article_title', 'article_subheading','article_text', 'article_date', 'article_background']
    # inlines = [ArticleInline]
    list_display = ('article_title', 'article_date')
    list_filter = ['article_date']
    search_fields = ['article_title']

    class Media:
        js = (
            '/static/tinymce/jquery.tinymce.min.js',
            '/static/tinymce/tinymce.min.js',
            '/static/tinymce/tiny_mce_init.js',
        )


admin.site.register(Article, ArticleAdmin)
