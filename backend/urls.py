from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from restaurant.views import event_inquiry, home, privacy_policy, reserve

urlpatterns = [
    path("", home, name="home"),
    path("rezervare/", reserve, name="reserve"),
    path("eveniment/", event_inquiry, name="event_inquiry"),
    path("politica-de-confidentialitate/", privacy_policy, name="privacy_policy"),
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
