# path("api/v1/categories/", views.category_api_list_view),
#     path("api/v1/categories/<int:id>/", views.category_detail_api_view),
#     path("api/v1/products/", views.product_api_list_view),
#     path("api/v1/products/<int:id>/", views.product_detail_api_view),
#     path("api/v1/reviews/", views.review_api_list_view),
#     path("api/v1/reviews/<int:id>/", views.review_detail_api_view),
#     path("api/v1/products/reviews/", views.product_review_api_view),
# ]
from django.urls import path
from . import views

urlpatterns = [
    path("categories/", views.CategoryListView.as_view()),
    path("categories/<int:id>/", views.CategoryDetailView.as_view()),
    path("", views.ProductListView.as_view()),
    path("<int:id>/", views.ProductDetialView.as_view()),
    path("reviews/", views.ReviewListView.as_view()),
    path("reviews/<int:id>/", views.ReviewDetailView.as_view()),
    path("ratings/", views.ProductReviewsListView.as_view())
]