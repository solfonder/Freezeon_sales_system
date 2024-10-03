from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api.v1 import api_views
from products.models import Info, Brand, Provider, Category  #InfoSet
from .views import HomePageView

router = routers.DefaultRouter()

# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.v1.urls', namespace='api')),
]
