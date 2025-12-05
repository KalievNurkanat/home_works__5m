from rest_framework import serializers
from .models import *


class CategoryListSerializers(serializers.ModelSerializer):
    products_count = serializers.IntegerField()
    class Meta:
        model = Category
        fields = ["id", "name", "products_count"]

    def get_product_count(self, product):
        return product.count_product()



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

class ProductRevSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField()
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "title", "average_rating", "reviews"]


    def get_average_rating(self, obj):
        if obj.average_rating is None:
            return 0
        return round(obj.average_rating, 2)
    
    
    def get_reviews(self, obj):
        qs = obj.review_set.all()
        return ReviewListSerializers(qs, many=True).data


# Review
class ReviewListSerializers(serializers.ModelSerializer):
     class Meta:
        model = Review
        fields = ["text", "stars"]


class ReviewDetailSerializers(serializers.ModelSerializer):
     class Meta:
        model = Review
        fields = "__all__"
