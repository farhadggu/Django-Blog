from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.views import View
from account.models import User
from django.contrib import messages
from django.db.models import Q
from urllib.parse import urlencode
from django.core.paginator import Paginator

from home.models import Post, Category, IPAddress
from .forms import CreatePostForm, UpdatePostForm, CreateUpdateCategoryForm, SearchForm
from .mixins import AuthorPostMixin, SuperUserMixin, AdminOrAuthorMixin
from .filters import PostFilter


class PanelView(SuperUserMixin, View):
    def get(self, request):
        users = User.objects.count()
        authors = User.objects.filter(is_author=True).count()
        posts = Post.objects.count()
        views = IPAddress.objects.count()
        return render(request, 'panel/panel.html', {'users':users, 'authors':authors, 'posts':posts, 'views':views})


class PostListsView(AdminOrAuthorMixin, ListView):
    def get(self, request):
        form = SearchForm()
        if request.user.is_admin:
            post = Post.objects.all()
            f = PostFilter(request.GET, queryset=post)
            posts = f.qs
        else:
            post = Post.objects.filter(user=self.request.user)
            f = PostFilter(request.GET, queryset=post)
            posts = f.qs
        paginator = Paginator(posts, 6)
        page_number = request.GET.get('page')
        data = request.GET.copy()
        if 'page' in data:
            del data['page']
        print(data, 'salam')
        page_obj = paginator.get_page(page_number)
        return render(request, 'panel/post_list.html', {'posts':page_obj, 'form':form, 'filter':f, 'data': urlencode(data)})



class SearchPostView(AdminOrAuthorMixin, ListView):
    def get(self, request):
        form = SearchForm(request.GET)
        data = request.GET.get('search')
        if 'search' in request.GET:
            posts = Post.objects.filter(Q(title__icontains=data) | Q(description__icontains=data))
        else:
            posts = Post.objects.all()
        f = PostFilter(request.GET, queryset=posts)
        posts = f.qs
        paginator = Paginator(posts, 6)
        page_number = request.GET.get('page')
        data = request.GET.copy()
        if 'page' in data:
            del data['page']
        page_obj = paginator.get_page(page_number)
        context = {
            'form':form, 'posts':page_obj,
            'filter':f, 'data': urlencode(data)
        }
        return render(request, 'panel/search_post_list.html', context)


class CreateNewPost(AdminOrAuthorMixin, View):
    form_class = CreatePostForm
    def get(self, request):
        form = self.form_class
        return render(request, 'panel/create_post.html', {'form':form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            if request.user.is_admin:
                new_post.status = 'p'
            else:
                new_post.status = 'd'
            new_post.save()
            form.save_m2m()
            messages.success(request, 'مقاله جدید ایجاد شد', 'success')
        else:
            messages.error(request, 'خطا!', 'danger')
        return redirect('panel:post_list')


class UpdatePostView(AuthorPostMixin, View):
    form_class = UpdatePostForm
    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, post_id):
        form = self.form_class(instance=self.post_instance)
        return render(request, 'panel/update_post.html', {'form':form})

    def post(self, request, post_id):
        form = self.form_class(request.POST, request.FILES, instance=self.post_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'مقاله جدید ایجاد شد', 'success')
            return redirect('panel:post_list')
        else:
            messages.error(request, 'خطا!', 'danger')
            return redirect('panel:update_post', post_id)


class DeletePostView(SuperUserMixin, View):
    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        post.delete()
        messages.success(request, 'مقاله حذف شد', 'success')
        return redirect('panel:post_list')


class CategoryListView(SuperUserMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'panel/category_list.html', {'categories':categories})


class CreateCategoryView(SuperUserMixin, View):
    form_class = CreateUpdateCategoryForm
    def get(self, request):
        form = self.form_class
        return render(request, 'panel/create_category.html', {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'دسته بندی شما ایجاد شد', 'success')
        else:
            messages.error(request, 'خطا!', 'danger')
        return redirect('panel:category_list')


class UpdateCategoryView(SuperUserMixin, View):
    form_class = CreateUpdateCategoryForm
    def setup(self, request, *args, **kwargs):
        self.instance_category = Category.objects.get(pk=kwargs['category_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, category_id):
        form = self.form_class(instance=self.instance_category)
        return render(request, 'panel/update_category.html', {'form':form})

    def post(self, request, category_id):
        form = self.form_class(request.POST, instance=self.instance_category)
        if form.is_valid():
            form.save()
            messages.success(request, 'دسته بندی شما ویرایش شد', 'success')
        else:
            messages.error(request, 'خطا!', 'danger')
        return redirect('panel:update_category', category_id)


class DeleteCategoryView(SuperUserMixin, View):
    def get(self, request, category_id):
        category = Category.objects.get(pk=category_id)
        category.delete()
        messages.success(request, 'دسته بندی حذف شد', 'success')
        return redirect('panel:category_list')