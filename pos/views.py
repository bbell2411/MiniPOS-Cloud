from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProductSerializer, CustomerSerializer
from .models import Product, Customer

class ProductListView(APIView):
    def get(self, request):
        """Get all products"""
        products=Product.objects.all()
        serializer=ProductSerializer(products, many=True)
        return Response(serializer.data)
    
class ProductDetailView(APIView):
    def get(self, request, product_id):
        """Get individual product"""
        try:
            product=Product.objects.get(id=product_id)
            serializer=ProductSerializer(product)
            return Response(serializer.data)
        
        except Product.DoesNotExist:
            return Response({"error":"Product not found."}, status=404)

class CustomerListView(APIView):
    def get(slef,request):
        """Get all Customers"""
        customers=Customer.objects.all()
        serializer=CustomerSerializer(customers,many=True)
        return Response(serializer.data)