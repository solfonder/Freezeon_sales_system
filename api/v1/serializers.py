from rest_framework import serializers
from products.models import Info, Brand, Provider, Category, InfoSet, Counterparty, CounterpartySaleType


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
    sale_type = serializers.StringRelatedField()
    set_info = serializers.SerializerMethodField()
    test_price = serializers.SerializerMethodField()

    class Meta:
        model = Info
        fields = '__all__'
        extra_fields = ['children']

    def get_set_info(self, obj):
        inheritances = InfoSet.objects.filter(parent_product=obj)
        children_info = [inheritance.child_product for inheritance in inheritances]
        return InfoSetSerializer(children_info, many=True).data

    def get_test_price(self, obj):
        request_data = self.context['request'].data.get('data', {})
        counterparty_name = request_data.get('counterparty')
        counterparty_markup = CounterpartySaleType.objects.filter(
            counterparty__counterparty_name=counterparty_name,
            sale_type=obj.sale_type
        ).values('counterparty_markup').first()

        if counterparty_markup:
            counterparty = Counterparty.objects.filter(
                counterparty_name=counterparty_name
            ).values('counterparty_risk').first()

            if counterparty:
                dealer_price = obj.dealer_price or 0
                risk_factor = (1 + counterparty['counterparty_risk'] / 100)
                markup_factor = (1 + counterparty_markup['counterparty_markup'] / 100)
                price = dealer_price * risk_factor * markup_factor
                return price

