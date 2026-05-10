from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from restaurant.views import home

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
