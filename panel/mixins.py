from django.http import Http404
from django.shortcuts import get_object_or_404
from home.models import Post


class SuperUserMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_admin:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404('صفحه مورد نظر یافت نشد')


class AdminOrAuthorMixin():
    def dispatch(self, request, *args, **kwargs):
            if request.user.is_admin or request.user.is_author:
                return super().dispatch(request, *args, **kwargs)
            else:
                raise Http404('صفحه مورد نظر یافت نشد')

class AuthorPostMixin():
    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['post_id'])
        if post.user == request.user or request.user.is_admin:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404('صفحه مورد نظر یافت نشد')