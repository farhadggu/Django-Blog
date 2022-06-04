from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls', namespace='account')),
    path('', include('home.urls', namespace='home')),
    path('tickets/', include('tickets.urls', namespace='tickets')),
    path('panel/', include('panel.urls', namespace='panel')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)