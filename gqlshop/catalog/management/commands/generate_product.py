from django.core.management.base import BaseCommand
from catalog.models import Product, Supplier, City, Category
from faker import Faker
import random


class Command(BaseCommand):

    def generate(self, amount=95):
        fake = Faker()
        categories = Category.objects.values_list('id', flat=True)
        suppliers = list(Supplier.objects.values_list('id', flat=True))
        for i in range(amount):
            product = Product.objects.create(
                name=fake.name(),
                price=random.random()*1000,
                description=fake.text(),
                category_id=random.choice(categories),
            )
            product.suppliers.add(
                *random.sample(suppliers, random.randint(1, len(suppliers)))
            )

    def handle(self, *args, **kwargs):
        self.generate()
        print("generate products finish")

