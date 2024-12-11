from django.urls import path

from .views import DownloadBlank, GetDeviceListView

urlpatterns = [
    path('example/',GetDeviceListView.as_view()),
    path('blank/', DownloadBlank.as_view()),
]
