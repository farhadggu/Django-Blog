from django import forms
from home.models import Post, Category


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('category', 'title', 'slug', 'description', 'image', 'slider_show')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['slug'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})


class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('category', 'title', 'slug', 'description', 'image', 'slider_show', 'status')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['slug'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        self.fields['status'].widget.attrs.update({'class': 'form-control'})


class CreateUpdateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('parent', 'is_sub', 'title', 'slug')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].widget.attrs.update({'class': 'form-control'})
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['slug'].widget.attrs.update({'class': 'form-control'})


class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control float-right', 'placeholder':'جستجو'}))