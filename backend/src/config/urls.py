from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from api.internal.v1.api import get_v1_api

urlpatterns = [path("v1/", get_v1_api().urls)]

if settings.DEBUG:
    urlpatterns += static("/media", document_root=settings.MEDIA_ROOT)
