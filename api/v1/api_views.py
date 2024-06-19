import logging
import pandas as pd
from django.db import transaction
from rest_framework import generics, filters, status
from rest_framework.pagination import PageNumberPagination

from products import models
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
        df = pd.read_excel('test.xlsx', 'Лист1')
        logger.info(df)
        products = []
        for index, row in df.iterrows():
            provider_name = row['provider_name_id']
            brand_name = row['brand_name_id']
            category_name = row['category_name_id']

            provider, created = Provider.objects.get_or_create(provider_name=provider_name)
            brand, created = Brand.objects.get_or_create(brand_name=brand_name)
            category, created = Category.objects.get_or_create(category_name=category_name)

            product_data = {
                'barcode': row['barcode'],
                'product_name': row['product_name'],
                'status': row['status'],
                'provider_name': provider,
                'brand_name': brand,
                'category_name': category,
                'stock': row['stock']
            }

            if not pd.isna(row['article']):
                product_data['article'] = row['article']

            products.append(product_data)

        Info.objects.bulk_create([Info(**data) for data in products])

        return Response("Data added successfully", status=status.HTTP_201_CREATED)


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
