import django_filters
from .models import *
from django_filters import DateFilter

class SearchFilter(django_filters.FilterSet):
    class Meta:
        model = Article
        fields = '__all__'
        exclude = ['title', 'content', 'updated', 'created']
