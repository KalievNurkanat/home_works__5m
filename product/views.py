from .models import *
from .serializers import *
from django.db.models import Avg
from django.db.models import Count
from rest_framework.permissions import *
from rest_framework.generics import *
# Categories

class OwnerRights(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.poster == request.user


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
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProductListSerializers
        return ProductDetailSerializers
    
    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)
    

class ProductDetialView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, OwnerRights]
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
    permission_classes = [IsAuthenticatedOrReadOnly, OwnerRights]
    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializers
    lookup_field = "id" 

