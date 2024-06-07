from django.urls import path
from . import api_views

app_name = 'api'

urlpatterns = [
    path('products/', api_views.InfoListView.as_view()),
    path('products/<pk>/', api_views.InfoDetailView.as_view()),
    path('brands/', api_views.BrandListView.as_view()),
    path('providers/', api_views.ProviderListView.as_view()),
    path('categories/', api_views.CategoryListView.as_view())
]
