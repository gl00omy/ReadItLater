from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = TaggableManager()
    favorites = models.ManyToManyField(User, related_name="favorite_article", blank=True)
    saves = models.ManyToManyField(User, related_name="save_article", blank=True)
    archived = models.ManyToManyField(User, related_name="archived_article", blank=True)
    highlights = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.title