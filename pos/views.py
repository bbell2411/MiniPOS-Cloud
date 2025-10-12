from rest_framework.views import APIView
from .serializers import ProductSerializer
from .models import Product

class ProductListView(APIView):
    def get(self, request):
        """Get all products"""
        products=Product.objects.all()
        serializer=ProductSerializer(products)
        return serializer.data