from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
# Create your views here.

# Categories
@api_view(http_method_names=["GET"])
def category_api_list_view(request):
    # step 1: Collect films from DB(QuerySet)
    categories = Category.objects.all()

    # step 2: Reformat QuerySet to list of dictionaries (Serializers)
    list_ = CategoryListSerializers(instance=categories, many=True).data

    # return Response
    return Response(
        data = list_ ,
        status = status.HTTP_200_OK,
    )

@api_view(["GET"])
def category_detail_api_view(request, id):
    try:
       category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                         data={"error":"Category not found"})
    item = CategoryDetailSerializers(category, many=False).data
    return Response(data=item, status=status.HTTP_200_OK)


# Products
@api_view(["GET"])
def product_api_list_view(request):
    products = Product.objects.all()

    list_ = ProductListSerializers(instance=products, many=True).data

    return Response(
        data = list_ ,
        status = status.HTTP_200_OK,
    )


@api_view(["GET"])
def product_detail_api_view(request, id):
    try:
       product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                         data={"error":"Product not found"})
    item = ProductDetailSerializers(product, many=False).data
    return Response(data=item, status=status.HTTP_200_OK)
    

# Review
@api_view(["GET"])
def review_api_list_view(request):
    reviews = Review.objects.all()

    list_ = ReviewListSerializers(instance=reviews, many=True).data

    return Response(
        data = list_ ,
        status = status.HTTP_200_OK,
    )


@api_view(["GET"])
def review_detail_api_view(request, id):
    try:
       review = Review.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                         data={"error":"Review not found"})
    item = ReviewDetailSerializers(review, many=False).data
    return Response(data=item, status=status.HTTP_200_OK)
    

    