from rest_framework import serializers
from .models import *


class CategoryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]
        

class CategoryDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


# Product
class ProductListSerializers(serializers.ModelSerializer):
     class Meta:
        model = Product
        fields = ["title"]

class ProductDetailSerializers(serializers.ModelSerializer):
     class Meta:
        model = Product
        fields = "__all__"


# Review
class ReviewListSerializers(serializers.ModelSerializer):
     class Meta:
        model = Review
        fields = ["text", "product"]

class ReviewDetailSerializers(serializers.ModelSerializer):
     class Meta:
        model = Review
        fields = "__all__"
