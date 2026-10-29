from django.urls import path

from .views import (
    CategoryListView,
    ProductListView,
    ProductDetailView,
    CreateOrderView,
    ValidateCouponView,
)


urlpatterns = [
    path(
        "categories/",
        CategoryListView.as_view(),
        name="category-list"
    ),

    path(
        "products/",
        ProductListView.as_view(),
        name="product-list"
    ),

    path(
        "products/<str:pk_or_slug>/",
        ProductDetailView.as_view(),
        name="product-detail"
    ),

    path(
        "orders/",
        CreateOrderView.as_view(),
        name="create-order"
    ),

    path(
        "validate-coupon/",
        ValidateCouponView.as_view(),
        name="validate-coupon"
    ),
]