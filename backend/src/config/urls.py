from django.urls import path

from api.internal.v1.api import get_api

urlpatterns = [path("v1/", get_api().urls)]
