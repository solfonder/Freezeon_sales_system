import logging

from rest_framework import serializers
from products.models import Info, Brand, Provider, Category, Counterparty, CounterpartySaleType, ProductIncluded


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


class CounterpartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Counterparty
        fields = '__all__'

class BaseInfoSerializer(serializers.ModelSerializer):
    brand_name = serializers.StringRelatedField()
    provider_name = serializers.StringRelatedField()
    category_name = serializers.StringRelatedField()
    sale_type = serializers.StringRelatedField()
    sale_price = serializers.SerializerMethodField()
    dealer_price_currency = serializers.StringRelatedField()
    recommended_price_currency = serializers.StringRelatedField()

    class Meta:
        model = Info
        fields = '__all__'

    def get_sale_price(self, obj):
        # request_data = self.context['request'].data.get('data', {})
        # counterparty_name = request_data.get('counterparty')
        # counterparty_markup = CounterpartySaleType.objects.filter(
        #     counterparty__counterparty_name=counterparty_name,
        #     sale_type=obj.sale_type
        # ).values('counterparty_markup').first()
        counterparty_name = self.context['request'].query_params.get('counterparty_name', None)
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
                risk_factor = (1 + (counterparty['counterparty_risk'] / 100))
                markup_factor = (1 + (counterparty_markup['counterparty_markup'] / 100))
                price = dealer_price * risk_factor * markup_factor
                return round(price, 2)

class IncludedProductSerializer(serializers.ModelSerializer):
    to_info = BaseInfoSerializer(read_only=True)

    class Meta:
        model = ProductIncluded
        fields = ['to_info', 'quantity']


class InfoSerializer(BaseInfoSerializer):
    included_products = IncludedProductSerializer(many=True, read_only=True)  # Removed source argument

    class Meta(BaseInfoSerializer.Meta):
        fields = '__all__'