from rest_framework import serializers
from products.models import Info, Brand, Provider, Category, InfoSet


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = '__all__'


class InfoSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Info
        fields = '__all__'


class InfoSerializer(serializers.ModelSerializer):
    brand_name = serializers.StringRelatedField()
    provider_name = serializers.StringRelatedField()
    category_name = serializers.StringRelatedField()
    set_info = serializers.SerializerMethodField()
    # test_price = serializers.SerializerMethodField()

    class Meta:
        model = Info
        fields = '__all__'
        extra_fields = ['children']

    def get_set_info(self, obj):
        inheritances = InfoSet.objects.filter(parent_product=obj)
        children_info = [inheritance.child_product for inheritance in inheritances]
        return InfoSetSerializer(children_info, many=True).data

    # def get_test_price(self, obj):
    #     price = Info.objects.filter(article=obj.article)..values('stock')[0]['stock']+100
    #     return price
