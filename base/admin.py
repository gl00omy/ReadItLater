from django.contrib import admin

# Register your models here.
from .models import Article, Category, Highlight, Author, SavedArticle, ArchivedArticle, FavoriteArticle

admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Highlight)
admin.site.register(Author)
admin.site.register(SavedArticle)
admin.site.register(ArchivedArticle)
admin.site.register(FavoriteArticle)
