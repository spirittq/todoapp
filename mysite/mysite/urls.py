from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('todoapp/', include('todoapp.urls')),
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='todoapp/', permanent=True)),
] + (static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +
     static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]