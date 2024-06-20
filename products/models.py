from django.db import models


class Provider(models.Model):
    provider_name = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

    def __str__(self):
        return self.provider_name


class Brand(models.Model):
    brand_name = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.brand_name


class Category(models.Model):
    category_name = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.category_name


class SaleType (models.Model):
    sale_type_ft = models.CharField(max_length=64, unique=True)
    sale_type_original = models.CharField(max_length=64, unique=False)
    provider = models.ManyToManyField(Provider)

    class Meta:
        verbose_name = 'Тип скидки'
        verbose_name_plural = 'Типы скидок'

    def __str__(self):
        return self.sale_type_ft


class Counterparty(models.Model):
    counterparty_name = models.CharField(max_length=64, unique=True)
    counterparty_risk = models.FloatField(default=0)

    class Meta:
        verbose_name = 'Контрагент'
        verbose_name_plural = 'Контрагенты'

    def __str__(self):
        return self.counterparty_name


class Info(models.Model):
    class Status(models.TextChoices):
        EOL = 'END OF LIFE'
        FS = 'FOR SALE'
        SS = 'STOP STOCKS'

    article = models.AutoField(primary_key=True)
    barcode = models.BigIntegerField()
    product_name = models.CharField(max_length=255)
    provider_name = models.ForeignKey(Provider,
                                      unique=False,
                                      on_delete=models.CASCADE)
    brand_name = models.ForeignKey(Brand,
                                   unique=False,
                                   on_delete=models.CASCADE)
    category_name = models.ForeignKey(Category,
                                      unique=False,
                                      on_delete=models.CASCADE)
    stock = models.IntegerField()
    sale_type = models.ForeignKey(SaleType,
                                 unique=False,
                                 on_delete=models.CASCADE,
                                 null=True)
    dealer_price = models.FloatField(default=0, null=True)
    recommended_price = models.FloatField(default=0, null=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        indexes = [
            models.Index(fields=['article', 'product_name'])
        ]

    def __str__(self):
        return self.product_name


class InfoSet(models.Model):
    parent_product = models.ForeignKey(Info,
                                       on_delete=models.CASCADE,
                                       related_name='children',
                                       unique=False)
    child_product = models.ForeignKey(Info, on_delete=models.CASCADE, related_name='parents')


class CounterpartySaleType(models.Model):
    counterparty = models.ForeignKey(Counterparty, on_delete=models.CASCADE)
    sale_type = models.ForeignKey(SaleType, on_delete=models.CASCADE)
    counterparty_markup = models.FloatField(default=None)
