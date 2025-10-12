from django.urls import path
from .views import ProductListView, ProductDetailView, CustomerListView

urlpatterns=[
    path("products/",ProductListView.as_view()),
    path("products/<int:product_id>/", ProductDetailView.as_view()),
    path("customers/",CustomerListView.as_view())
]