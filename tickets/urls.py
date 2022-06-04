from django.urls import path
from . import views


app_name = 'tickets'
urlpatterns = [
    path('', views.TicketPage.as_view(), name='tickets'),
    path('contact-us/', views.TicketView.as_view(), name='contactus'),
]
