from django.urls import path
from .views import ProductListView, ProductDetailView, CustomerListView, CustomerDetailView, PaymentsListView, PaymentDetailView, OrderListView, OrderDetailView, OrderItemsListView, PaymentIntentView

urlpatterns=[
    path("products/",ProductListView.as_view()),
    path("products/<int:product_id>/", ProductDetailView.as_view()),
    path("customers/",CustomerListView.as_view()),
    path("customers/<int:customer_id>/", CustomerDetailView.as_view()),
    path("payments/",PaymentsListView.as_view()),
    path("payments/<int:payment_id>/", PaymentDetailView.as_view()),
    path("orders/", OrderListView.as_view()),
    path("orders/<int:order_id>/", OrderDetailView.as_view()),
    path("orders/<int:order_id>/items/", OrderItemsListView.as_view()),
    path("orders/<int:order_id>/items/<int:item_id>/", OrderItemsListView.as_view()),
    path("orders/<int:order_id>/payment-intent/", PaymentIntentView.as_view())
]