from django.urls import path
from . import api_views

app_name = 'api'

urlpatterns = [
    path('products/', api_views.InfoListView.as_view()),
    path('products/<pk>/', api_views.InfoDetailView.as_view())
]
