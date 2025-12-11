from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from django.db.models import Avg
from django.db.models import Count

# Categories
@api_view(http_method_names=["GET", "POST"])
def category_api_list_view(request):
    if request.method == "GET":
        # step 1: Collect products from DB(QuerySet)
        categories = Category.objects.all().annotate(products_count=Count("product"))

        # step 2: Reformat QuerySet to list of dictionaries (Serializers)
        list_ = CategoryListSerializers(instance=categories, many=True).data

        # return Response
        return Response(
            data = list_ ,
            status = status.HTTP_200_OK,
        )
    
    elif request.method == "POST":
        category_validate = CategoryValidateSerializer(data=request.data)
        if not category_validate.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=category_validate.errors)
        
        name = category_validate.validated_data.get("name")
        category = Category.objects.create(
            name=name
            )
        category.save()
        return Response(status=status.HTTP_201_CREATED, data=CategoryDetailSerializers(category).data)


@api_view(["GET", "PUT", "DELETE"])
def category_detail_api_view(request, id):
    try:
       category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                         data={"error":"Category not found"})
    
    if request.method == "GET":
        item = CategoryDetailSerializers(category, many=False).data
        return Response(data=item, status=status.HTTP_200_OK)  
    
    elif request.method == 'PUT':
        category_validate = CategoryValidateSerializer(data=request.data)
        if not category_validate.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=category_validate.errors)
        
        category.name = category_validate.validated_data.get("name")
        category.save()
        return Response(data=CategoryDetailSerializers(category).data, status=status.HTTP_201_CREATED)  
    
    elif request.method =="DELETE":
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)        

# Products
@api_view(["GET", "POST"])
def product_api_list_view(request):
    if request.method == "GET":
        products = Product.objects.all()

        list_ = ProductListSerializers(instance=products, many=True).data

        return Response(
            data = list_ ,
            status = status.HTTP_200_OK,
        )
    
    elif request.method == "POST":
        product_validate = ProductValidateSerializers(data=request.data)
        if not product_validate.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=product_validate.errors)
        
        
        title = product_validate.validated_data.get("title")
        description = product_validate.validated_data.get("description")
        price = product_validate.validated_data.get("price")
        category_id = product_validate.validated_data.get("category_id")

        product = Product.objects.create(
            title=title, description=description, price=price, category_id=category_id,
        )
        product.save()

        return Response(status=status.HTTP_201_CREATED, data=ProductDetailSerializers(product).data)


@api_view(["GET", "PUT", "DELETE"])
def product_detail_api_view(request, id):
    try:
       product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                         data={"error":"Product not found"})
    
    if request.method == "GET":
        item = ProductDetailSerializers(product, many=False).data
        return Response(data=item, status=status.HTTP_200_OK)

        
    elif request.method == 'PUT':
        product_validate = ProductValidateSerializers(data=request.data)
        if not product_validate.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=product_validate.errors)
              
        product.title = product_validate.validated_data.get("title")
        product.description = product_validate.validated_data.get("description")
        product.price = product_validate.validated_data.get("price")
        product.category_id = product_validate.validated_data.get("category_id")
        product.save()
        return Response(data=ProductDetailSerializers(product).data, status=status.HTTP_201_CREATED)  
    
    elif request.method =="DELETE":
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# Review
@api_view(["GET", "POST"])
def review_api_list_view(request):
    if request.method == "GET":
        reviews = Review.objects.all()

        list_ = ReviewListSerializers(instance=reviews, many=True).data

        return Response(
            data = list_ ,
            status = status.HTTP_200_OK,
        )
    
    elif request.method == "POST":
        review_validate = ReviewValidateSerializers(data=request.data)
        if not review_validate.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=review_validate.errors)
        
        
        text = review_validate.validated_data.get("text")
        stars = review_validate.validated_data.get("stars")
        product_id = review_validate.validated_data.get("product_id")
        
        review = Review.objects.create(
            text=text, stars=stars, product_id=product_id,
        )
        review.save()
        return Response(status=status.HTTP_201_CREATED, data=ReviewDetailSerializers(review).data)


@api_view(["GET", "PUT", "DELETE"])
def review_detail_api_view(request, id):
    try:
       review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                         data={"error":"Review not found"})
    
    if request.method == "GET":
        item = ReviewDetailSerializers(review, many=False).data
        return Response(data=item, status=status.HTTP_200_OK)
    
    elif request.method == "PUT":
        review_validate = ReviewValidateSerializers(data=request.data)
        if not review_validate.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=review_validate.errors)
    
        review.text = review_validate.validated_data.get("text")
        review.stars = review_validate.validated_data.get("stars")
        review.product_id = review_validate.validated_data.get("product_id")
        
        review.save()
        return Response(data=ReviewDetailSerializers(review).data, status=status.HTTP_201_CREATED)  
    
    elif request.method =="DELETE": 
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(["GET"])
def product_review_api_view(request):
    queryset = Product.objects.all().annotate(average_rating=Avg("review__stars"))
    serializer_class = ProductRevSerializer(instance=queryset, many=True).data
    return Response(data=serializer_class, status=status.HTTP_200_OK)