from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Product)
class Admin(admin.ModelAdmin):
    list_display = ("title", "category")
    list_editable = ("category",)

admin.site.register(Category)
admin.site.register(Review)
