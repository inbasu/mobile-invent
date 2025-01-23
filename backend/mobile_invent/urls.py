from django.urls import path

from .views import (DownloadBlank, GetDeviceListView, GetITItemsListView,
                    GetStoresListView, GetUsersListView, HandleActionView)

urlpatterns = [
    path('items/',GetDeviceListView.as_view()),
    path('items/it/',GetITItemsListView.as_view()),
    path('stores/',GetStoresListView.as_view()),
    path('users/',GetUsersListView.as_view()),
    path('blank/', DownloadBlank.as_view()),
    path('action/', HandleActionView.as_view()),
]
