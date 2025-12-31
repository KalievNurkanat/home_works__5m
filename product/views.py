from product.models import Category, Product, Review
from product.serializers import (CategoryListSerializers,
                               CategoryDetailSerializers,
                               ProductListSerializers,
                               ProductDetailSerializers,
                               ReviewListSerializers,
                               ReviewDetailSerializers,
                               ProductReviewsSerializer)
from django.db.models import Avg
from django.db.models import Count
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from common.permissions import IsOwnerOrModerator, IsAuthenticatedOrReadOnly, IsModerator
# Categories

class CategoryListView(ListCreateAPIView):
    queryset = Category.objects.annotate(products_count=Count("product"))
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_serializer_class(self):
        if self.request.method == "GET":
            return CategoryListSerializers
        return CategoryDetailSerializers
    

class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Category.objects.annotate(products_count=Count("product"))
    serializer_class = CategoryDetailSerializers
    lookup_field = "id"

# Products
class ProductListView(ListCreateAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly | IsModerator]
    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProductListSerializers
        return ProductDetailSerializers
    
    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)
    

class ProductDetialView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrModerator]
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializers
    lookup_field = "id"

class ProductReviewsListView(ListAPIView):
    queryset = Product.objects.all().annotate(
        rating=Avg("review__stars")
    )
    serializer_class = ProductReviewsSerializer


# Review
class ReviewListView(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Review.objects.all()
    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReviewListSerializers
        return ReviewDetailSerializers
    
    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)
    
class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrModerator]
    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializers
    lookup_field = "id" 

