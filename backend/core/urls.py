from django.urls import include, path

urlpatterns = [
        path('mobile/', include('mobile_invent.urls')),
]

