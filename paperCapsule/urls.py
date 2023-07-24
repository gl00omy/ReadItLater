from django.urls import path
from .views import ( 
    ArticleListView, 
    ArticleDetailView, 
    FavoritedArticleListView, 
    SavedArticleListView,
    ArticleCreateView,
    ArticleUpdateView,
    ArticleDeleteView
    )
from . import views


urlpatterns = [
    path('', ArticleListView.as_view(), name='paperCapsule-home'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('article_favorite/<int:pk>', views.article_favorite, name="article-favorite"),
    path('favorited_articles/<int:user_id>/', FavoritedArticleListView.as_view(), name='favorited_articles'),
    path('article_save/<int:pk>', views.article_save, name="article-save"),
    path('saved_articles/<int:user_id>/', SavedArticleListView.as_view(), name='saved_articles'),
    path('article/archive/<int:pk>/', views.article_archive, name='article_archive'),
    path('user/<int:user_id>/archived/', views.ArchivedArticleListView.as_view(), name='archived_articles'),
    path('article/unarchive/<int:pk>/', views.article_unarchive, name='article_unarchive'),
    path('search_articles/', views.search_articles, name='search-articles'),
   
    path('add_tag/<int:article_id>/', views.add_tag_to_article, name='add_tag'),

    path('article/new/', ArticleCreateView.as_view(), name='article-create'),
    path('article/<int:pk>/update/', ArticleUpdateView.as_view(), name='article-update'),
    path('article/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article-delete'),


]

