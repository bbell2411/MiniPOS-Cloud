from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .serializers import ProductSerializer, CustomerSerializer, PaymentsSerializer, OrderSerializer, OrderItemSerializer
from .models import Product, Customer, Payments, Order, OrderItem

class ProductListView(APIView):
    def get(self, request):
        """Get all products"""
        products=Product.objects.all()
        serializer=ProductSerializer(products, many=True)
        return Response(serializer.data)
    
class ProductDetailView(APIView):
    def get(self, request, product_id):
        try:
            product=Product.objects.get(id=product_id)
            serializer=ProductSerializer(product)
            return Response(serializer.data)
        
        except Product.DoesNotExist:
            return Response({"error":"Product not found."}, status=404)

class CustomerListView(APIView):
    def get(self,request):
        customers=Customer.objects.all()
        serializer=CustomerSerializer(customers,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer= CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)        
        
class CustomerDetailView(APIView):
    def get(self, request,customer_id):
        try:
            customer=Customer.objects.get(id=customer_id)
            serializer=CustomerSerializer(customer)
            return Response(serializer.data)
            
        except Customer.DoesNotExist:
            return Response({"error":"customer not found."},status=404)
        
    def patch(self,request,customer_id):
        try:
            customer= Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response({"error":"Customer not found."},status=404)
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, customer_id):
        try:
            customer= Customer.objects.get(id=customer_id)
            customer.delete()
            return Response(status=204)
        except Customer.DoesNotExist:
            return Response({"error":"Customer not found."},status=404)
        
class PaymentsListView(APIView):
    def get(self, request):
        payments=Payments.objects.all()
        serializer=PaymentsSerializer(payments,many=True)
        return Response(serializer.data)

class PaymentDetailView(APIView):
    def  get(self, request,payment_id):
        try:
            payment=Payments.objects.get(id=payment_id)
            serializer=PaymentsSerializer(payment)
            return Response(serializer.data)
        except Payments.DoesNotExist:
            return Response({"error":"Payment not found."},status=404)

class OrderListView(APIView):
    def get(self, request):
        orders=Order.objects.all()
        serializer=OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer=OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class OrderDetailView(APIView):
    def get(self,request,order_id):
        try:
            order=Order.objects.get(id=order_id)
            serializer=OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({"error":"Order not found."},status=404)
        
class OrderItemsListView(APIView):
    def get(self,request,order_id, item_id=None):
        try:
            order=Order.objects.get(id=order_id)
            
            if item_id:
                item=order.items.get(id=item_id)
                serializer=OrderItemSerializer(item)
            else:
                items=order.items.all()
                serializer=OrderItemSerializer(items,many=True)
            return Response(serializer.data)
                
        except OrderItem.DoesNotExist:
            return Response({"error":"Item not found."}, status=404)
        except Order.DoesNotExist:
            return Response({"error":"Order not found."},status=404)
        
    def post(self,request,order_id):
            try:
                order=Order.objects.get(id=order_id)
            except Order.DoesNotExist:
                return Response({"error":"Order not found."}, status=404)
            serializer=OrderItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(order=order)
                return Response(serializer.data,status=201)
            return Response(serializer.errors,status=400)
                