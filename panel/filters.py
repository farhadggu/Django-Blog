import django_filters
from django import forms
from home.models import Post


class PostFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Post.STATUS)

    class Meta:
        model = Post
        fields = ['status']