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
from django.utils.text import Truncator
from .forms import ArticleForm

AVERAGE_READING_SPEED = 200

@login_required
def home(request):
    articles = Article.objects.all().order_by('-date_posted')
    saved_articles = articles.filter(saves=request.user)
    unsaved_articles = articles.exclude(saves=request.user)
    tags = Tag.objects.all()
    max_title_chars = 50  # Adjust this to your desired character limit for the title
    max_content_chars = 200 
    

    # Get the tags associated with unsaved articles
    unsaved_articles_tags = Tag.objects.filter(article__in=unsaved_articles).distinct()

    for article in articles:
        article.display_title = Truncator(article.title).chars(max_title_chars)
        article.display_content = Truncator(article.content).chars(max_content_chars)



    context = {
        'articles': articles,
        #'last_three_articles': last_three_articles,
        #'saved_articles': saved_articles,
        #'tags': tags,
        'unsaved_articles': unsaved_articles,
        'unsaved_articles_tags': unsaved_articles_tags,
    }
    return render(request, 'paperCapsule/home.html', context)


class ArticleListView(ListView):
    model = Article
    template_name = 'paperCapsule/home.html'
    context_object_name = 'articles'
    ordering = ['-date_posted']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        max_chars = 200  # Adjust the number of characters you want to show

        for article in context['articles']:
            # Truncate the article content
            article.display_content = Truncator(article.content).chars(max_chars)

            # Add a flag to indicate if the article content is truncated or not
            article.is_truncated = len(article.content) > max_chars

        # Get the tags associated with unsaved articles
        #unsaved_article_tags = Tag.objects.filter(article__in=self.get_queryset().exclude(saves=self.request.user)).distinct()
        #context['unsaved_article_tags'] = unsaved_article_tags

        return context


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
    form_class = ArticleForm
    #fields = ['title', 'content', 'tags']

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

class FavoritedArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'paperCapsule/favorited_articles.html'
    context_object_name = 'articles'

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Article.objects.filter(favorites__id=user_id)

    @staticmethod
    def calculate_reading_time(text):
        words = len(text.split())
        minutes = math.ceil(words / AVERAGE_READING_SPEED)
        return minutes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_favorited_articles = context['articles']
        max_chars = 100  # Adjust the number of characters you want to show

        # Truncate the article content and add a flag to indicate if it is truncated
        for article in user_favorited_articles:
            article.display_content = Truncator(article.content).chars(max_chars)
            article.is_truncated = len(article.content) > max_chars

            # Calculate the estimated reading time for each favorited article
            article.estimated_reading_time = self.calculate_reading_time(article.content)

        # Retrieve the favorited articles tags and add them to the context
        context['saved_articles_tags'] = Tag.objects.filter(
            article__in=user_favorited_articles
        ).distinct()

        return context

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

class SavedArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'paperCapsule/saved_articles.html'
    context_object_name = 'articles'

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Article.objects.filter(saves__id=user_id)

    @staticmethod
    def calculate_reading_time(text):
        words = len(text.split())
        minutes = math.ceil(words / AVERAGE_READING_SPEED)
        return minutes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_saved_articles = context['articles']
        saved_articles_tags = Tag.objects.filter(article__in=user_saved_articles).distinct()
        context['saved_articles_tags'] = saved_articles_tags
        max_chars = 100  # Adjust the number of characters you want to show

        # Truncate the article content and add a flag to indicate if it is truncated
        for article in user_saved_articles:
            article.display_content = Truncator(article.content).chars(max_chars)
            article.is_truncated = len(article.content) > max_chars

            # Calculate the estimated reading time for each saved article
            article.estimated_reading_time = self.calculate_reading_time(article.content)

        return context

    
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


class ArchivedArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'paperCapsule/archived_articles.html'
    context_object_name = 'articles'

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Article.objects.filter(archived__id=user_id)

    @staticmethod
    def calculate_reading_time(text):
        words = len(text.split())
        minutes = math.ceil(words / AVERAGE_READING_SPEED)
        return minutes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_archived_articles = context['articles']
        max_chars = 100  # Adjust the number of characters you want to show

        # Truncate the article content and add a flag to indicate if it is truncated
        for article in user_archived_articles:
            article.display_content = Truncator(article.content).chars(max_chars)
            article.is_truncated = len(article.content) > max_chars

            # Calculate the estimated reading time for each archived article
            article.estimated_reading_time = self.calculate_reading_time(article.content)

        # Retrieve the saved articles tags and add them to the context
        context['saved_articles_tags'] = Tag.objects.filter(article__in=user_archived_articles).distinct()

        return context


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
        saved_articles = Article.objects.filter(saves=request.user)
        articles = saved_articles.filter(content__contains=searched)
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

def all_tags(request):
    tags = Tag.objects.all()
    return render(request, 'paperCapsule/all_tags.html', {'tags': tags})

def tagged_articles(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)

    # Get the articles with the specified tag
    articles_with_tag = Article.objects.filter(tags=tag)

    # Filter out the saved articles for the current user
    unsaved_articles = articles_with_tag.exclude(saves=request.user)
    unsaved_article_tags = Tag.objects.filter(article__in=unsaved_articles).distinct()

    return render(request, 'paperCapsule/tagged_articles.html', {'tag': tag, 'articles': unsaved_articles, 'unsaved_article_tags': unsaved_article_tags})

@login_required
def tagged_saved_articles(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    saved_articles_with_tag = Article.objects.filter(tags=tag, saves=request.user)

    context = {
        'tag_name': tag_name,
        'articles': saved_articles_with_tag,
        'saved_articles_tags': Tag.objects.filter(article__in=saved_articles_with_tag).distinct(),
    }
    return render(request, 'paperCapsule/tagged_saved_articles.html', context)


class TaggedSavedArticlesListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'paperCapsule/tagged_saved_articles.html'
    context_object_name = 'articles'

    def get_queryset(self):
        tag_name = self.kwargs['tag_name']
        tag = get_object_or_404(Tag, name=tag_name)
        saved_articles_with_tag = Article.objects.filter(tags=tag, saves=self.request.user)

        for article in saved_articles_with_tag:
            # Calculate the estimated reading time for each saved article
            article.estimated_reading_time = self.calculate_reading_time(article.content)

        return saved_articles_with_tag

    @staticmethod
    def calculate_reading_time(text):
        words = len(text.split())
        minutes = math.ceil(words / AVERAGE_READING_SPEED)
        return minutes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_name = self.kwargs['tag_name']
        user_favorited_articles = context['articles']
        context['tag_name'] = tag_name
        max_chars = 100  # Adjust the number of characters you want to show

        # Truncate the article content and add a flag to indicate if it is truncated
        for article in user_favorited_articles:
            article.display_content = Truncator(article.content).chars(max_chars)
            article.is_truncated = len(article.content) > max_chars

            # Calculate the estimated reading time for each favorited article
            article.estimated_reading_time = self.calculate_reading_time(article.content)


        # Retrieve the saved articles tags and add them to the context
        context['saved_articles_tags'] = Tag.objects.filter(
            article__in=context['articles']
        ).distinct()

        return context