from django.urls import path
from . import views


app_name = 'panel'
urlpatterns = [
    path('home/', views.PanelView.as_view(), name='home'),
    path('post-list/', views.PostListsView.as_view(), name='post_list'),
    path('create-post/', views.CreateNewPost.as_view(), name='create_post'),
    path('update-post/<int:post_id>/', views.UpdatePostView.as_view(), name='update_post'),
    path('delete-post/<int:post_id>/', views.DeletePostView.as_view(), name='delete_post'),
    path('category-list/', views.CategoryListView.as_view(), name='category_list'),
    path('create-category/', views.CreateCategoryView.as_view(), name='create_category'),
    path('update-category/<int:category_id>/', views.UpdateCategoryView.as_view(), name='update_category'),
    path('delete-category/<int:category_id>/', views.DeleteCategoryView.as_view(), name='delete_category'),
    path('post-list/search/', views.SearchPostView.as_view(), name='search'),
]

