from rest_framework import serializers
from .models import Product, Order, OrderItem, Customer, Payments

class ProductSerializer(serializers.ModelSerializer):
    price=serializers.IntegerField(min_value=0)
    class Meta:
        model= Product
        fields="__all__"

class OrderSerializer(serializers.ModelSerializer):
    total=serializers.IntegerField(min_value=0)
    class Meta:
        model=Order
        fields="__all__"
        read_only_fields = ["total", "created_at", "created_by"]

class OrderItemSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1)
    class Meta:
        model= OrderItem
        fields="__all__"
        read_only_fields=["subtotal"]
        
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model= Customer
        fields="__all__"
        
class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Payments
        fields="__all__"
        read_only_fields=["amount","created_at"]