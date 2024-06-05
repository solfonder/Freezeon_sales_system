from rest_framework import generics
from rest_framework.pagination import CustomLimitPagination
from products.models import Info
from .serializers import InfoSerializer
from django_filters.rest_framework import DjangoFilterBackend


# @api_view()
# def all_products(requset):
#     product = Info.objects.all()
#     product_serializer = ProductSerializer(product, many=True)
#     return Response(product_serializer.data)

class InfoListView(generics.ListAPIView):
    queryset = Info.objects.all()
    serializer_class = InfoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'
    pagination_class = CustomLimitPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class InfoDetailView(generics.RetrieveAPIView):
    queryset = Info.objects.all()
    serializer_class = InfoSerializer

# class InfoSearchView(generics.ListAPIView):
#     queryset = Info.objects
#     # pagination_class =
#
#     def get(self, request, *args, **kwargs):
#         response = request.GET
