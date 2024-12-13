from django.urls import path

from .views import DownloadBlank, GetDeviceListView, GetStoresListView

urlpatterns = [
    path('items/',GetDeviceListView.as_view()),
    path('stores/',GetStoresListView.as_view()),
    path('blank/', DownloadBlank.as_view()),
]
