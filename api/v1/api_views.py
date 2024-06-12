import logging
import pandas as pd
import numpy as np
from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination
from products.models import Info, Provider, Brand, Category
from .serializers import InfoSerializer, ProviderSerializer, BrandSerializer, CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import Response

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# @api_view()
# def all_products(requset):
#     product = Info.objects.all()
#     product_serializer = ProductSerializer(product, many=True)
#     return Response(product_serializer.data)

class InfoListView(generics.ListAPIView):
    queryset = Info.objects.all()
    serializer_class = InfoSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['^article', '^product_name', '=status']
    filterset_fields = '__all__'
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        df = pd.read_excel('test.xlsx')
        arr = df.values.T
        return Response(arr)


class InfoDetailView(generics.RetrieveAPIView):
    queryset = Info.objects.all()
    serializer_class = InfoSerializer

class ProviderListView(generics.ListAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class BrandListView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# class InfoSearchView(generics.ListAPIView):
#     queryset = Info.objects
#     # pagination_class =
#
#     def get(self, request, *args, **kwargs):
#         response = request.GET
