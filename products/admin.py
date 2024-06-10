from django.contrib import admin
from .models import Info, Brand, Provider, Category, Info_Set

@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
        list_display = ('article', 'product_name', 'provider_name', 'brand_name', 'status', 'set', 'category_name', 'stock')
# Register your models here.
