from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from . models import Article
from taggit.models import Tag
from . forms import TagForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import math

AVERAGE_READING_SPEED = 200

def home(request):
    articles = Article.objects.all().order_by('-date_posted')
    last_three_articles = articles.exclude(saves__in=[request.user])[:3]
    saved_articles = articles.filter(saves=request.user)
    
    
    context = {
        'articles': articles,
        'last_three_articles': last_three_articles,
        'saved_articles': saved_articles,
       
    }
    return render(request, 'paperCapsule/home.html', context)

class ArticleListView(ListView):
    model = Article
    template_name = 'paperCapsule/home.html'
    context_object_name = 'articles'
    ordering = ['-date_posted']

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'paperCapsule/article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = context['article']

        # Calculate the estimated reading time based on the article's content
        estimated_reading_time = self.calculate_reading_time(article.content)
        context['estimated_reading_time'] = estimated_reading_time

        return context

    @staticmethod
    def calculate_reading_time(text):
        words = len(text.split())
        minutes = math.ceil(words / AVERAGE_READING_SPEED)
        return minutes

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ['title', 'content', 'tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ['title', 'content', 'tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        article = self.get_object()
        if self.request.user == article.author:
            return True
        return False
    
class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    success_url = '/'

    def test_func(self):
        article = self.get_object()
        if self.request.user == article.author:
            return True
        return False
    
    
    

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


