from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.urls import reverse
from ckeditor.fields import RichTextField

class Article(models.Model):
    title = models.CharField(max_length=100)
    #content = models.TextField()
    content = RichTextField(blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = TaggableManager()
    favorites = models.ManyToManyField(User, related_name="favorite_article", blank=True)
    saves = models.ManyToManyField(User, related_name="save_article", blank=True)
    archived = models.ManyToManyField(User, related_name="archived_article", blank=True)
    is_archived = models.BooleanField(default=False)
    highlights = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    def archive(self):
        self.is_archived = True
        self.save()

    def unarchive(self):
        self.is_archived = False
        self.save()

    def get_absolute_url(self):
        return reverse('article-detail', kwargs={'pk': self.pk})