from django.urls import path, include
from . import views


app_name = 'home'

bucket_urls = [
    path('', views.BucketHome.as_view(), name='bucket'),
    path('delete_obj/<str:key>/', views.DeleteBucketObject.as_view(), name='delete_obj_bucket'),
    path('download_obj/<str:key>/', views.DownloadBucketObject.as_view(), name='download_obj_bucket'),
]

urlpatterns = [
    path('navbar/', views.NavbarView.as_view(), name='navbar'),
    path('sidebar/<int:post_id>/', views.SidebarView.as_view(), name='sidebar'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('', views.HomeView.as_view(), name='home'),
    path('detail/<slug:slug>/', views.DetailView.as_view(), name='detail'),
    path('category/<slug:slug>/', views.CategoryView.as_view(), name='category'),
    path('like/<int:post_id>/', views.AddLikeView.as_view(), name='post_like'),
    path('add_reply/<int:post_id>/<int:comment_id>/', views.AddReplyView.as_view(), name='post_reply'),
    path('contact-us/', views.ContactUsView.as_view(), name='contact-us'),
    path('bucket/', include(bucket_urls))
]
