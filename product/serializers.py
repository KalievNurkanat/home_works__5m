from rest_framework import serializers
from .models import *
from rest_framework.serializers import ValidationError

# Category
class CategoryListSerializers(serializers.ModelSerializer):
    products_count = serializers.IntegerField()
    class Meta:
        model = Category
        fields = ["id", "name", "products_count"]


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
    product_id = serializers.IntegerField(required=True)

    class Meta:
        model = Review
        fields = ["id", "text", "stars", "product_id"]

    def create(self, validated_data):
        product_id = validated_data.pop("product_id")

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError(
                {"product_id": "Product not found"}
            )
        return Review.objects.create(
            product=product,
            **validated_data
        )


class ProductReviewsSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    review = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "title", "review", "rating"]

    def get_rating(self, obj):
        if obj.rating is None:
            return 0
        return round(obj.rating, 2)
    

    def get_review(self, obj):
        qs = obj.review_set.all()
        return ReviewListSerializers(qs, many=True).data
    


class ReviewDetailSerializers(serializers.ModelSerializer):
     class Meta:
        model = Review
        fields = "__all__"
