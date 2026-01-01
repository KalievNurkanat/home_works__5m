from django.contrib import admin
from product.models import Product, Category, Review

# Register your models here.
@admin.register(Product)
class Admin(admin.ModelAdmin):
    list_display = ("title", "category_id")
    list_editable = ("category_id",)

admin.site.register(Category)
admin.site.register(Review)

