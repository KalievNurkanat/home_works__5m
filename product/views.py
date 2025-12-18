from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from django.db.models import Avg
from django.db.models import Count
from rest_framework.generics import *
from rest_framework.views import APIView
# Categories

class CategoryListView(ListAPIView, CreateAPIView):
    queryset = Category.objects.annotate(products_count=Count("product"))
    def get_serializer_class(self):
        if self.request.method == "GET":
            return CategoryListSerializers
        return CategoryDetailSerializers
    

class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.annotate(products_count=Count("product"))
    serializer_class = CategoryDetailSerializers
    lookup_field = "id"

# Products
class ProductListView(ListAPIView, CreateAPIView):
    queryset = Product.objects.all()
    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProductListSerializers
        return ProductDetailSerializers
    

class ProductDetialView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializers
    lookup_field = "id"

class ProductReviewsListView(ListAPIView):
    queryset = Product.objects.all().annotate(
        rating=Avg("review__stars")
    )
    serializer_class = ProductReviewsSerializer


# Review
class ReviewListView(ListAPIView, CreateAPIView):
    queryset = Review.objects.all()
    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReviewListSerializers
        return ReviewDetailSerializers
    
class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializers
    lookup_field = "id" 

