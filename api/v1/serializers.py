from rest_framework import serializers
from products.models import Info, Brand, Provider, Category, Info_Set


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

    class Meta:
        model = Info
        fields = '__all__'
        extra_fields = ['children']

    def get_set_info(self, obj):
        inheritances = Info_Set.objects.filter(parent_product=obj)
        children_info = [inheritance.child_product for inheritance in inheritances]
        return InfoSetSerializer(children_info, many=True).data
