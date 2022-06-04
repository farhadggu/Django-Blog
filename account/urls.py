from django.urls import path, re_path
from . import views


app_name = 'account'
urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('verify-phone/', views.UserRegisterVerifyCodeView.as_view(), name='verify_code'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('edit-profile/', views.EditProfileView.as_view(), name='edit-profile'),
    path('update-phone/', views.UpdatePhoneNumberView.as_view(), name='update_phone'),
    path('activate-email/', views.ActivateEmailView.as_view(), name='email-activate'),
    path('activate/<uidb64>/<token>/<email>/', views.Activate.as_view(), name='activate'),
    path('change-username/', views.ChangeUsernameView.as_view(), name='change_username'),
    path('author/<str:username>/', views.AuthorView.as_view(), name='author'),
]
