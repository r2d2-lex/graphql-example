from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(
        "City",
        related_name='suppliers',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    supplier = models.ForeignKey(
        Supplier,
        related_name='products',
        on_delete=models.CASCADE,
    )
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name

