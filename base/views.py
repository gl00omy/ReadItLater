from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from requests import Response
from .models import Article, Highlight, Category, Author, SavedArticle, Highlight, ArchivedArticle, FavoriteArticle
from .filters import SearchFilter
from django.contrib.auth.models import User
from django.views.generic.detail import DetailView
from tkinter import *
from django.views.decorators.http import require_POST

def home(request):
    articles = Article.objects.all()
    myFilter = SearchFilter(request.GET, queryset=articles)
    articles = myFilter.qs
    context = {'articles': articles, 'myFilter': myFilter }
    return render(request, 'base/home.html', context)

def article(request, pk):
    article = Article.objects.get(id=pk)
    is_saved = False
    if request.user.is_authenticated:
        saved_articles = request.user.saved_articles.all()
        is_saved = saved_articles.filter(article=article).exists()

    context = {'article': article,
                'is_saved': is_saved,}
    return render(request, 'base/article.html', context)

def LoginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user= authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')


    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

    return render(request, 'base/login_register.html', {'form': form})

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    context = {'user': user}
    return render(request, 'base/profile.html', context)

#@api_view(['POST'])
@login_required(login_url='login')
#def save_article(request, pk):
 #   article = Article.objects.get(pk=pk)
  #  user = request.user
   # saved_article = SavedArticle.objects.create(user=user, article=article)
    #saved_article.save()
    #messages.success(request, 'Article added to your saved articles!')
    #return redirect(request, 'base/save_article/html', pk=pk)

@login_required
def save_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    saved_article=SavedArticle.objects.filter(user=request.user, article=article).first()

    if saved_article:
        saved_article.delete()
        article.is_saved = False
    else:
        SavedArticle.objects.create(user=request.user, article=article)
        article.is_saved = True
        article.is_archived = False


    article.save()
    messages.success(request, 'Article saved!')

    return redirect('saved_articles')

@login_required
#def saved_articles(request):
#    saved_articles = SavedArticle.objects.filter(user=request.user.saved_articles.all())
#   context = {'saved_articles': saved_articles}
#   return render(request, 'base/saved_articles.html', context)

def saved_articles(request):
    saved_articles = request.user.savedarticle_set.all()
    context = {'saved_articles': saved_articles}
    return render(request, 'base/saved_articles.html', context)

@login_required
def archive_article(request, id):
    article = get_object_or_404(Article, id=id)
    archived_article=ArchivedArticle.objects.create(user=request.user, article=article)
    saved_article = SavedArticle.objects.filter(user=request.user, article=article)
    if article.archived:
        if saved_article:
            saved_article.delete()
        messages.success(request, 'The article has been archived.')
        return redirect('archived_articles')
    else:
        messages.warning(request, 'This article is already archived.')
        return redirect(request.META.get('HTTP_REFERER'))


@login_required
def archived_articles(request):
    archived_articles = request.user.archivedarticle_set.all()
    context = {'archived_articles': archived_articles}
    return render(request, 'base/archived_articles.html', context)

@login_required
def favorite_article(request, id):
    article = get_object_or_404(Article, id=id)
    favorite_article=FavoriteArticle.objects.create(user=request.user, article=article)
    favorite_article.save()
    return redirect('favorite_articles')




@login_required
def favorite_articles(request):
    favorite_articles = request.user.favoritearticle_set.all()
    context = {'favorite_articles': favorite_articles}
    return render(request, 'base/favorite_articles.html', context)

@login_required
def unsave_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    saved_article = SavedArticle.objects.filter(user=request.user, article=article).first()
    if saved_article:
        saved_article.delete()
        article.is_saved = False
        article.is_archived = False
        article.save()
        messages.success(request, 'Article unsaved!')
    return redirect(request.META.get('HTTP_REFERER'), id=article_id)


@login_required
def unarchive_article(request, id):
    article = get_object_or_404(Article, id=id)
    request.user.archived_articles.remove(article)
    request.user.saved_articles.add(article)
    return redirect('archived_articles')


@login_required
def unsaved_article(request, id):
    article = get_object_or_404(Article, id=id)
    if article in request.user.saved_articles.all():
        request.user.saved_articles.remove(article)
        messages.success(request, f'The article "{article.title}" has been unsaved!')
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def unarchived_article(request, id):
    article = get_object_or_404(Article, id=id)
    if article in request.user.archivedarticle_set.all():
        request.user.archivedarticle_set.remove(article)
        messages.success(request, f'The article "{article.title}" has been unarchived!')
    if article not in request.user.saved_articles.all():
        request.user.saved_articles.add(article)
    return redirect('archived_articles', id=id)



class ArticleDetailView(DetailView):
    model = Article
    template_name = 'base/article_detail.html'


def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    return render(request, 'base/article_detail.html', {'article': article, 'favorites': article.favorites})

def reading_mode(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    return render(request, 'base/reading_mode.html', {'article': article})

def enableReadingMode():
    window = Tk()
    window.location.href = "{% url 'reading_mode' article_id=article.id %}"

@require_POST
def create_highlight(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    user = request.user
    text = request.POST.get('text')
    highlight = Highlight.objects.create(article=article, user=user, text=text)
    return redirect('base/reading_mode.html', article_id=article.id)