from django import forms
from .models import Article

class TagForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'tags',     
        ]
