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


class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=5, max_length=30)


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
    

class ProductValidateSerializers(serializers.Serializer):
    title = serializers.CharField(min_length=5, max_length=255)
    description = serializers.CharField(max_length=200, required=False)
    price = serializers.IntegerField()
    category_id = serializers.IntegerField()

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError("Category doesnt exists")
        return category_id



# Review
class ReviewListSerializers(serializers.ModelSerializer):
     class Meta:
        model = Review
        fields = ["text", "stars"]


class ReviewDetailSerializers(serializers.ModelSerializer):
     class Meta:
        model = Review
        fields = "__all__"


class ReviewValidateSerializers(serializers.Serializer):
    text = serializers.CharField(max_length=200)
    stars = serializers.IntegerField(min_value=1, max_value=10)
    product_id = serializers.IntegerField()

    def validate_product_id(self, product_id):
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError("Product doesnt exists")
        return product_id