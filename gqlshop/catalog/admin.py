from django.contrib import admin
from django.db.models import Prefetch, Sum
from .models import Category, City, CurrencyRate, Product, Supplier
import requests

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'sells',
        'name',
        'price',
        'supplier',
        'city',
        'get_categories_str',
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        prefetch_qs = Category.objects.only('name')
        prefetch = Prefetch(
            'categories',
            queryset=prefetch_qs
        )
        qs = qs.prefetch_related(prefetch).select_related(
            'supplier__city',
        ).annotate(total_sum=Sum('orderproducts__quantity'))
        return qs

    @staticmethod
    def city(obj):
        return obj.supplier.city

    def sells(self, obj):
        return obj.total_sum or 'x'

    def get_categories_str(self, obj):
        return ', '.join([c.name for c in obj.categories.all()])

    get_categories_str.short_description = 'Categories'


class CurrencyRateAdmin(admin.ModelAdmin):

    actions = ['update_currency_rates',]

    def update_currency_rates(self, request, queryset):
        for rate in queryset:
            pair = '{}RUB'.format(rate.currency.upper())
            response = requests.get(
                'https://www.freeforexapi.com/api/live?pairs={}'.format(pair)
            )
            data = response.json()
            rate.rate = data['rates'][pair]['rate']
            rate.save(update_fields=['rate'])


admin.site.register(Category)
admin.site.register(City)
admin.site.register(Product, ProductAdmin)
admin.site.register(Supplier)
admin.site.register(CurrencyRate, CurrencyRateAdmin)