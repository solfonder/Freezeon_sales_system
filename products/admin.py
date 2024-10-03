from django.contrib import admin
from .models import Info, Brand, Provider, Category, Counterparty, CounterpartySaleType, SaleType

class ProductAdmin(admin.ModelAdmin):
    list_display = ['article', 'product_name', 'is_bundle']
    list_filter = ['is_bundle']
    search_fields = ['article']

    # Для комплектов разрешаем выбирать другие товары
    filter_horizontal = ('included_products',)

    def get_queryset(self, request):
        # Исключаем товары, которые включены в другие комплекты (если требуется)
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.exclude(is_bundle=False, included_products__isnull=False)
        return queryset

class BrandAdmin(admin.ModelAdmin):
    list_display = ['brand_name']
    search_fields = ['brand_name']

class ProviderAdmin(admin.ModelAdmin):
    list_display = ['provider_name']
    search_fields = ['provider_name']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name']
    search_fields = ['category_name']

class CounterpartyAdmin(admin.ModelAdmin):
    list_display = ['counterparty_name']
    search_fields = ['counterparty_name']

class CounterpartySaleTypeAdmin(admin.ModelAdmin):
    list_display = ['counterparty', 'sale_type', 'counterparty_markup']
    search_fields = ['counterparty_name']

class SaleTypeAdmin(admin.ModelAdmin):
    list_display = ['sale_type_ft']
    search_fields = ['sale_type_ft']

admin.site.register(SaleType, SaleTypeAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Counterparty, CounterpartyAdmin)
admin.site.register(CounterpartySaleType, CounterpartySaleTypeAdmin)
admin.site.register(Info, ProductAdmin)