import logging

import numpy as np
import pandas as pd
from django.db import transaction
from rest_framework import generics, filters, status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

from products import models
from products.models import Info, Provider, Brand, Category, SaleType, Counterparty, Currency
from .serializers import InfoSerializer, ProviderSerializer, BrandSerializer, CategorySerializer, CounterpartySerializer
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
    pagination_class = LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

        # Создание модели если не существует
    def get_or_create_model(self, model, field_name, value):
        return model.objects.get_or_create(**{field_name: value})[0]

    def create_product_data(self, row, provider, brand, category, sale_type,
                            prefix=''):
        dealer_price_currency = Currency.objects.get(code__exact=row['ВалютаДилерскойЦены']) if pd.notna(
            row['ВалютаДилерскойЦены']) and row['ВалютаДилерскойЦены'].strip() else None
        recommended_price_currency = Currency.objects.get(code__exact=row['ВалютаРИЦ']) if pd.notna(
            row['ВалютаРИЦ']) and row['ВалютаРИЦ'].strip() else None
        return {
            'barcode': row[f'ШК{prefix}'] if prefix else row['ШКпозиции'],
            'product_name': row[f'Блок{prefix}'] if prefix else row[
                'Позиция'],
            'product_series': row['Серия'] if pd.notna(
                row['Серия']) and row['Серия'].strip() else None,
            'provider_name': provider,
            'brand_name': brand,
            'category_name': category,
            'stock': None if prefix and pd.isna(
                row.get(f'НаличиеБлок{prefix}')) else row.get(
                f'НаличиеБлок{prefix}') if prefix else (
                None if pd.isna(row.get('НаличиеПозиция')) else row.get(
                    'НаличиеПозиция')),
            'sale_type': sale_type,
            'stock_name': None if prefix and pd.isna(
                row.get(f'ОстаткиБлок{prefix}')) else row.get(
                f'ОстаткиБлок{prefix}') if prefix else (
                None if pd.isna(row.get('ОстаткиПозиция')) else row.get(
                    'ОстаткиПозиция')),
            'dealer_price': None if pd.isna(row['Дилерская']) else row['Дилерская'],
            'recommended_price': None if pd.isna(row['РИЦ']) else row['РИЦ'],
            'dealer_price': row['Дилерская'],
            'recommended_price': row['РИЦ'],
            'is_bundle': not pd.isna(row['Блок1']),
        }


    def post(self, request, *args, **kwargs):
        # excel_products = pd.read_excel(
        #     'Z:\\1. ФРИЗОН ТРЕЙД\\4. Отдел продаж\\1. ПРАЙСЫ для Клиентов\\4. IT\\18. Модули для системы скидок\\4. Выгрузка Системы скидок\\Выгрузка Системы скидок.xlsx',
        #     'Прайс-лист').replace(np.nan, None)
        excel_products = pd.read_excel('D:/Projects/test.xlsx', 'Лист1')

        for _, row in excel_products.iterrows():
            logger.info(f'Позиция -----> {row["Артикулпозиции"]} -> {row["Артикул1"]} + {row["Артикул2"]} + {row["Артикул3"]}')
            provider = self.get_or_create_model(Provider, 'provider_name',
                                                row['Поставщик'])
            brand = self.get_or_create_model(Brand, 'brand_name', row['Бренд'])
            category = self.get_or_create_model(Category, 'category_name',
                                                row['ТипОборудованияПозиция'])
            sale_type = self.get_or_create_model(
                SaleType, 'sale_type_ft', row['Типскидки']) if pd.notna(
                row['Типскидки']) and row['Типскидки'].strip() else None
            product_data = self.create_product_data(row, provider, brand, category,
                                               sale_type)

            if not pd.isna(row['Артикулпозиции']):
                if Info.objects.filter(article=row['Артикулпозиции']).exists():
                    continue
                product_data['article'] = row['Артикулпозиции']

            if product_data['is_bundle']:
                bundle = Info.objects.create(**product_data)
                included_products = []

                for i in range(1, 4):
                    if not pd.isna(row[f'Блок{i}']):
                        # Пробуем преобразовать значение артикула в целое число
                        try:
                            article = int(row[f'Артикул{i}']) if pd.notna(
                                row[f'Артикул{i}']) else None
                        except (ValueError, TypeError):
                            article = None

                        if article is not None:
                            logger.info(
                                f'^Комплект {article}')
                        else:
                            logger.warning(
                                f"Артикул {row[f'Артикул{i}']} не может быть преобразован в int")

                        category = self.get_or_create_model(Category,
                                                            'category_name',
                                                            row[
                                                                f'ТипОборудованияБлок{i}']) if pd.notna(
                            row[f'ТипОборудованияБлок{i}']) and row[
                                                                                                   f'ТипОборудованияБлок{i}'].strip() else None

                        included_product = self.create_product_data(row,
                                                                    provider,
                                                                    brand,
                                                                    category,
                                                                    sale_type,
                                                                    prefix=str(
                                                                        i))

                        # Проверка для третьего блока с аксессуарами
                        if i == 3:
                            sale_type_accessory = self.get_or_create_model(
                                SaleType, 'sale_type_ft',
                                row['ТипСкидкиАксессуара']) if pd.notna(
                                row['ТипСкидкиАксессуара']) and row[
                                                                   'ТипСкидкиАксессуара'].strip() else None
                            included_product['sale_type'] = sale_type_accessory
                            included_product['dealer_price'] = row[
                                'ЦенаАксессуара']

                        #Проверка на наличие артикула и добавление товара в комплект
                        # if article is not None and not Info.objects.filter(
                        #         article=article).exists():
                        if article is not None:
                            included_product['article'] = article
                            included_products.append(included_product)
                        else:
                            logger.warning(
                                f"Пропущен товар с Артикулом {row[f'Артикул{i}']} - артикул отсутствует или товар уже существует")

                # Проверка артикулов перед фильтрацией
                if included_products:
                    # Создаем список артикулов для фильтрации
                    article_list = []

                    for data in included_products:
                        article = data['article']
                        if article and not Info.objects.filter(
                                article=article).exists():
                            # Если артикул не существует, добавляем в базу
                            Info.objects.create(**data)
                        else:
                            # Если артикул существует, просто добавляем его в список для фильтрации
                            article_list.append(article)

                    logger.debug(
                        f"Список артикулов для фильтрации: {article_list}")

                    # Получаем сохраненные артикулы из базы данных
                    saved_included_products = Info.objects.filter(
                        article__in=article_list)
                    logger.info(saved_included_products.values('article'))

                    # Устанавливаем связанные продукты в комплект
                    bundle.included_products.set(saved_included_products)
                else:
                    logger.warning("Нет товаров для сохранения в комплекте")
            else:
                if Info.objects.filter(article=row['Артикулпозиции']).exists():
                    continue
                Info.objects.create(**product_data)


        return Response(status=status.HTTP_201_CREATED)


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

class CounterPartyListView(generics.ListAPIView):
    queryset = Counterparty.objects.all()
    serializer_class = CounterpartySerializer
