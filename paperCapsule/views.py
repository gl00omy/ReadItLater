from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    ListView, 
    DetailView
)
from . models import Article
from taggit.models import Tag
from . forms import TagForm
from django.contrib.auth.decorators import login_required


def home(request):
    context = {
        'articles': Article.objects.all()
    }
    return render(request, 'paperCapsule/home.html', context)

class ArticleListView(ListView):
    model = Article
    template_name = 'paperCapsule/home.html'
    context_object_name = 'articles'
    ordering = ['-date_posted']

class ArticleDetailView(DetailView):
    model = Article

@login_required
def article_favorite(request, pk):
    article = get_object_or_404(Article, id=pk)
    is_saved = article.saves.filter(id=request.user.id).exists()

    if is_saved:
        if article.favorites.filter(id=request.user.id).exists():
            # The article is currently favorited by the user, so we want to unfavorite it.
            article.favorites.remove(request.user)
        else:
            # The article is not favorited by the user, so we want to favorite it.
            article.favorites.add(request.user)
    return redirect(request.META.get("HTTP_REFERER"))

class FavoritedArticleListView(ListView):
    model = Article
    template_name = 'paperCapsule/favorited_articles.html'
    context_object_name = 'articles'

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Article.objects.filter(favorites__id=user_id)

@login_required
def article_save(request, pk):
    article = get_object_or_404(Article, id=pk)
    is_saved = article.saves.filter(id=request.user.id).exists()
    is_favorited = article.favorites.filter(id=request.user.id).exists()

    if is_saved:
        # The article is currently saved by the user, so we want to unsave it.
        article.saves.remove(request.user)
        # If the article was favorited, remove it from favorites as well.
        if is_favorited:
            article.favorites.remove(request.user)
    else:
        # The article is not saved by the user, so we want to save it.
        article.saves.add(request.user)
    return redirect(request.META.get("HTTP_REFERER"))

class SavedArticleListView(ListView):
    model = Article
    template_name = 'paperCapsule/saved_articles.html'
    context_object_name = 'articles'

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Article.objects.filter(saves__id=user_id)
    
@login_required
def article_archive(request, pk):
    article = get_object_or_404(Article, id=pk)
    is_saved = article.saves.filter(id=request.user.id).exists()
    is_archived = article.archived.filter(id=request.user.id).exists()

    if is_saved:
        if is_archived:
            # The article is currently archived by the user, so we want to unarchive it.
            article.archived.remove(request.user)
        else:
            # The article is not archived by the user, so we want to archive it.
            article.archived.add(request.user)
            # If the article was saved, remove it from saved articles as well.
            article.saves.remove(request.user)

    return redirect(request.META.get("HTTP_REFERER"))


class ArchivedArticleListView(ListView):
    model = Article
    template_name = 'paperCapsule/archived_articles.html'
    context_object_name = 'articles'

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Article.objects.filter(archived__id=user_id)

@login_required
def article_unarchive(request, pk):
    article = get_object_or_404(Article, id=pk)
    is_saved = article.saves.filter(id=request.user.id).exists()
    is_archived = article.archived.filter(id=request.user.id).exists()

    if is_archived:
        # The article is currently archived by the user, so we want to unarchive it.
        article.archived.remove(request.user)
        # If the article was saved, remove it from saved articles as well.
        if is_saved:
            article.saves.remove(request.user)
        else:
            # If the article was not saved, add it back to saved articles.
            article.saves.add(request.user)

    return redirect(request.META.get("HTTP_REFERER"))

@login_required
def search_articles(request):
    if request.method == "POST":
        searched = request.POST['searched']
        articles = Article.objects.filter(content__contains=searched)
        return render(request, 'paperCapsule/search_articles.html', {'searched': searched, 'articles': articles})
    else:
        return render(request, 'paperCapsule/search_articles.html')




@login_required
def add_tag_to_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    if request.method == 'POST':
        tag_name = request.POST.get('tag_name')
        if tag_name:
            article.tags.add(tag_name)

    return render(request, 'paperCapsule/add_tag.html', {'article': article})