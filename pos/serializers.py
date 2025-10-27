from rest_framework import serializers
from .models import Product, Order, OrderItem, Customer, Payments, PaymentIntent

class ProductSerializer(serializers.ModelSerializer):
    price=serializers.IntegerField(min_value=0)
    class Meta:
        model= Product
        fields="__all__"

class OrderSerializer(serializers.ModelSerializer):
    total=serializers.IntegerField(min_value=0, read_only=True)
    customer = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), 
        required=True
    )
    class Meta:
        model=Order
        fields="__all__"
        read_only_fields = ["total", "created_at"]

class OrderItemSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(),
        required=True
    )
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        required=True
    )

    class Meta:
        model= OrderItem
        fields="__all__"
        read_only_fields=["subtotal"]
        
class CustomerSerializer(serializers.ModelSerializer):
    name=serializers.CharField(required=True, allow_blank=False)
    class Meta:
        model= Customer
        fields="__all__"
    def validate_name(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError("Name must be a string.")
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty.")
        return value
    
class PaymentIntentSerializer(serializers.ModelSerializer):
    class Meta:
        model= PaymentIntent
        fields = ["id", "order", "amount", "client_secret", "status", "created_at"]
        read_only_fields = ["id", "order", "client_secret", "status", "created_at", "amount"]
        
class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Payments
        fields="__all__"
        read_only_fields=["order", "amount","created_at", "status"]
        