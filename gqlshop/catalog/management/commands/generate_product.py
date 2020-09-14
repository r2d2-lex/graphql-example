from django.core.management.base import BaseCommand
from catalog.models import Product, Supplier, City, Category
from faker import Faker
import random


class Command(BaseCommand):

    def generate(self, amount=95):
        fake = Faker()
        categories = list(Category.objects.values_list('id', flat=True))
        suppliers = Supplier.objects.values_list('id', flat=True)
        for i in range(amount):
            product = Product.objects.create(
                name=fake.name(),
                price=random.random()*1000,
                description=fake.text(),
                supplier_id=random.choice(suppliers),
            )
            product.categories.add(
                *random.sample(categories, random.randint(1, len(categories)))
            )

    def handle(self, *args, **kwargs):
        self.generate()
        print("generate products finish")

