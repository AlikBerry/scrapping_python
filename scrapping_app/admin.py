from django.contrib import admin
from scrapping_app.models import *


class ProductItemTabularInline(admin.TabularInline):
    model = ProductItem
    extra = 2

@admin.register(ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    inlines = [ProductItemTabularInline]


