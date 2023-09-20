from django import forms
from .models import Article

class TagForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'tags',     
        ]

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'content', 'tags')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
        }