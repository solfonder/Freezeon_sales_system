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

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True,
                            verbose_name="Код валюты")
    name = models.CharField(max_length=50, verbose_name="Название валюты", null=True)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="Курс обмена", default=1.0)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления курса")

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"

    def __str__(self):
        return self.code


class Comment(models.Model):
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.comment_text


class Info(models.Model):
    class Status(models.TextChoices):
        EOL = 'END OF LIFE'
        FS = 'FOR SALE'
        SS = 'STOP STOCKS'

    article = models.AutoField(primary_key=True)
    barcode = models.BigIntegerField()
    product_name = models.CharField(max_length=255)
    product_series = models.CharField(max_length=255, null=True)
    provider_name = models.ForeignKey(Provider,
                                      unique=False,
                                      null=True,
                                      on_delete=models.CASCADE)
    brand_name = models.ForeignKey(Brand,
                                   unique=False,
                                   null=True,
                                   on_delete=models.CASCADE)
    category_name = models.ForeignKey(Category,
                                      unique=False,
                                      null=True,
                                      on_delete=models.CASCADE)
    stock = models.IntegerField(default=0, null=True)
    sale_type = models.ForeignKey(SaleType,
                                 unique=False,
                                 on_delete=models.CASCADE,
                                 null=True)
    price_name = models.CharField(max_length=255, null=True)
    stock_name = models.CharField(max_length=255, null=True)
    dealer_price_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="dealer_prices", null=True)
    recommended_price_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="recomended_prices", null=True)
    dealer_price = models.FloatField(default=0, null=True)
    recommended_price = models.FloatField(default=0, null=True)
    is_bundle = models.BooleanField(default=False)
    # included_products = models.ManyToManyField('self', blank=True, symmetrical=False)
    comments = models.ManyToManyField(Comment, blank=True, symmetrical=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        indexes = [
            models.Index(fields=['article', 'product_name'])
        ]

    def __str__(self):
        return self.product_name


class ProductIncluded(models.Model):
    from_info = models.ForeignKey(Info, on_delete=models.CASCADE, related_name='included_products')
    to_info = models.ForeignKey(Info, on_delete=models.CASCADE, related_name='included_in_info')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('from_info', 'to_info')

    def __str__(self):
        return f"{self.from_info.product_name} includes {self.quantity} of {self.to_info.product_name}"


class CounterpartySaleType(models.Model):
    counterparty = models.ForeignKey(Counterparty, on_delete=models.CASCADE)
    sale_type = models.ForeignKey(SaleType, on_delete=models.CASCADE)
    counterparty_markup = models.FloatField(default=None)
