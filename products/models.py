from django.db import models


class Provider(models.Model):
    provider_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.provider_name


class Brand(models.Model):
    brand_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.brand_name


class Category(models.Model):
    category_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.category_name


class Info(models.Model):
    class Status(models.TextChoices):
        EOL = 'END OF LIFE'
        FS = 'FOR SALE'
        SS = 'STOP STOCKS'

    article = models.BigIntegerField(primary_key=True)
    barcode = models.BigIntegerField()
    product_name = models.CharField(max_length=255)
    provider_name = models.ForeignKey(Provider,
                                      unique=False,
                                      on_delete=models.CASCADE)
    brand_name = models.ForeignKey(Brand,
                                   unique=False,
                                   on_delete=models.CASCADE)
    status = models.CharField(max_length=20,
                              choices=Status.choices,
                              default=Status.SS,
                              unique=False)
    set = models.BooleanField(default=False, unique=False)
    category_name = models.ForeignKey(Category,
                                      unique=False,
                                      on_delete=models.CASCADE)
    stock = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['article', 'product_name'])
        ]

    def __str__(self):
        return self.product_name


class InfoSet(models.Model):
    parent_product = models.ForeignKey(Info,
                                       on_delete=models.CASCADE,
                                       related_name='sets',
                                       unique=False)
    child_product = models.ForeignKey(Info, on_delete=models.CASCADE)
