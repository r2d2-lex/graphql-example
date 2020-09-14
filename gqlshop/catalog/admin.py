from django.contrib import admin
from django.db.models import Prefetch
from .models import Category, City, Product, Supplier


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'price',
        'supplier',
        'city',
        'get_categories_str',
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # prefetch_qs = Category.objects.only('name')
        # prefetch = Prefetch(
        #     'categories',
        #     queryset=prefetch_qs
        # )
        # qs = qs.prefetch_related(prefetch)
        return qs

    @staticmethod
    def city(obj):
        return obj.supplier.city

    def get_categories_str(self, obj):
        return ', '.join([c.name for c in obj.categories.all()])

    get_categories_str.short_description = 'categories'


admin.site.register(Category)
admin.site.register(City)
admin.site.register(Product, ProductAdmin)
admin.site.register(Supplier)
