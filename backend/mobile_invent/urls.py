from django.urls import path

from .views import DownloadBlank, GetDeviceListView

urlpatterns = [
    path('items/',GetDeviceListView.as_view()),
    path('blank/', DownloadBlank.as_view()),
]
