from rest_framework import generics
from rest_framework.pagination import CustomLimitPagination
from products.models import Info, Provider, Brand, Category
from .serializers import InfoSerializer, ProviderSerializer, BrandSerializer, CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


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
    pagination_class = CustomLimitPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


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
