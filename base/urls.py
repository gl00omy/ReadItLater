from django.urls import path 
from . import views
from .views import article_detail, reading_mode, favorite_article



urlpatterns = [
    path('', views.home, name="home"),

    path('login/', views.LoginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),


    path('article/<str:pk>/', views.article, name="article"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
  
    path('save_article/<int:article_id>/', views.save_article, name='save_article'),
    path('saved_articles/', views.saved_articles, name='saved_articles'),

    path('archived_articles/', views.archived_articles, name='archived_articles'),
    path('archive_article/<int:id>/', views.archive_article, name='archive_article'),

    path('favorite_article/<int:id>/', views.favorite_article, name='favorite_article'),
    path('favorite_articles/', views.favorite_articles, name='favorite_articles'),

    path('unsave_article/<int:article_id>/', views.unsave_article, name='unsave_article'),


    path('unarchive_article/<int:id>/', views.unarchive_article, name='unarchive_article'),
    path('unsaved_article/<int:id>/', views.unsaved_article, name='unsaved_article'),
    path('unarchived_article/<int:id>/', views.unarchived_article, name='unarchived_article'),


    
    
    path('article_detail', views.ArticleDetailView.as_view(), name='article-detail'),

    path('articles/<int:article_id>/reading_mode/', views.reading_mode, name='reading_mode'),
    path('articles/<int:article_id>/', article_detail, name='article_detail'),
    path('reading_mode/<int:article_id>/', reading_mode, name='reading_mode'),
    path('article/<int:article_id>/highlight/', views.create_highlight, name='create_highlight'),


   
]