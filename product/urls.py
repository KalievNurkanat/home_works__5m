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
    path("category/", views.category_api_list_view),
    path("category/<int:id>/", views.category_detail_api_view),
    path("product/", views.product_api_list_view),
    path("product/<int:id>/", views.product_detail_api_view),
    path("review/", views.review_api_list_view),
    path("review/<int:id>/", views.review_detail_api_view)
]