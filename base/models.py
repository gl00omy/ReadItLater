from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    email = models.EmailField()

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200)
    #abstract
    #journal ref
    #comments
    #authors
    #submitter
    content = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category)
    favorites = models.PositiveIntegerField(default=0)
    saved = models.BooleanField(default=False)
    archived = models.BooleanField(default=True)
    

    #image = models.ImageField(upload_to='images/', blank=True, null=True)
    #author = models.ForeignKey(Author)
    def __str__(self):
        return self.title
    
class Highlight(models.Model):
   
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    highlighted_text = models.TextField()
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    #content = models.TextField()
   # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.article.title}"

class SavedArticle(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_articles')
    #article = models.ForeignKey(Article, on_delete=models.CASCADE)
    #saved_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s saved {self.article.title}"   

class ArchivedArticle(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_articles')
    #article = models.ForeignKey(Article, on_delete=models.CASCADE)
    #saved_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    archived_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s archived {self.article.title}"   
    
class FavoriteArticle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    date_favorited = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s favorited {self.article.title}"   
