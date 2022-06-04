#==>Library Import
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Count
from django.db.models import Q
from django.views import View
#==>Local Import
from .models import Category, Post, Like, Comment
from .forms import CommentForm, SearchForm
from . import tasks


class NavbarView(View):
    def get(self, request):
        categories = Category.objects.filter(is_sub=False)
        form = SearchForm()
        return render(request, 'inc/navbar.html', {'categories':categories, 'form':form})


class SidebarView(View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        most_visited_post = Post.objects.annotate(p_count=Count('visit_count')).order_by('-p_count')
        return render(request, 'inc/sidebar.html', {'post':post, 'most_visited_post':most_visited_post})


class SearchView(View):
    def get(self, request):
        search = request.GET.get('search')
        posts = Post.objects.filter(Q(title__icontains=search)|Q(description__icontains=search))
        paginator = Paginator(posts, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'post_list.html', {'posts':page_obj})


class HomeView(View):
    def get(self, request):
        # {% for book in object.book_author.all|slice:":4" %}
        slider_posts = Post.objects.filter(slider_show=True, status='p')
        vip_posts = Post.objects.filter(vip=True, status='p')[:2]
        posts = Post.objects.filter(status='p')
        most_visited_posts = Post.objects.annotate(p_count=Count('visit_count')).order_by('-p_count')[:4]
        categories = Category.objects.filter(is_sub=False)
        return render(request, 'home.html', {'slider_posts':slider_posts, 'vip_posts':vip_posts, 'posts':posts, 'categories':categories, 'most_visited_posts':most_visited_posts})


class DetailView(View):
    form_class = CommentForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, slug=kwargs['slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class
        # Post View Count
        ip_address = request.user.ip_address
        self.post_instance.visit_count.add(ip_address)
        comments = self.post_instance.comment_post.filter(is_reply=False)
        return render(request, 'detail.html', {'post':self.post_instance, 'form':form, 'comments':comments})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request, 'کامنت شما افزوده شد', 'success')
            return redirect('home:detail', kwargs['slug'])

            

class CategoryView(View):
    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        posts = Post.objects.filter(category=category)
        paginator = Paginator(posts, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'category.html', {'posts':page_obj, 'category':category})


class AddLikeView(View):
    def post(self, request, post_id):
        last_url = request.META.get('HTTP_REFERER')
        user = request.user
        like_exists = Like.objects.filter(user=user).exists()
        if like_exists:
            messages.success(request, 'پست مورد نظر قبلا لایک شده است', 'info')
        else:
            Like.objects.create(user=user, post_id=post_id)
            messages.success(request, 'پست مورد نظر لایک شد', 'success')
        return redirect(last_url)


class AddReplyView(View):
    def post(self, request, post_id, comment_id):
        post = get_object_or_404(Post, pk=post_id)
        print(post)
        comment = get_object_or_404(Comment, pk=comment_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            new_reply = form.save(commit=False)
            new_reply.user = request.user
            new_reply.post = post
            new_reply.reply = comment
            new_reply.is_reply = True
            new_reply.save()
            messages.success(request, 'پاسخ شما ایجاد شد', 'success')
            return redirect('home:detail', post.slug)


class ContactUsView(View):
    def get(self, request):
        return render(request, 'contactus.html', {})


class BucketHome(View):
    template_name = 'bucket.html'
    def get(self, request):
        objects = tasks.all_bucket_objects_task()
        return render(request, self.template_name, {'objects':objects})


class DeleteBucketObject(View):
    def get(self, request, key):
        tasks.delete_object_task.delay(key)
        messages.success(request, 'تصویر انتخابی به زودی حذف خواهد شد', 'success')
        return redirect('home:bucket')
        

class DownloadBucketObject(View):
    def get(self, request, key):
        tasks.download_object_task.delay(key)
        messages.success(request, 'تصویر انتخابی به زودی دانلود خواهد شد', 'success')
        return redirect('home:bucket')