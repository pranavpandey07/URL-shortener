from rest_framework.routers import SimpleRouter
from django.urls import path
from .views import URLViewSet

urlpatterns = [
    path('create_short_url/', URLViewSet.as_view({'post': 'create'}), name='urls-create'),
    path('<str:name>/', URLViewSet.as_view({'get': 'redirect_to_long_url'}), name='redirect_to_long_url')

]


