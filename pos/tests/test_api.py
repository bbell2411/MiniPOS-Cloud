import pytest
from rest_framework.test import APIClient
from pos.models import Product,Customer, Order, Payments, OrderItem

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def customers():
    customers=[]
    customers.append(Customer.objects.create(name="one", email="email1",phone=123456789))
    customers.append(Customer.objects.create(name="two", email="email2",phone=123456788))
    customers.append(Customer.objects.create(name="three", email="email3",phone=123456787))
    return customers

@pytest.fixture
def products():
    products=[]
    products.append(Product.objects.create(name="pone", price=100, stock=50))
    products.append(Product.objects.create(name="ptwo", price=200, stock=30))
    products.append(Product.objects.create(name="pthree", price=250, stock=100))
    products.append(Product.objects.create(name="pfour", price=5000, stock=10))
    return products

@pytest.fixture
def orders(customers,products):
    order1=Order.objects.create(customer=customers[0],status="pending")
    
    #manually add items to designated tab
    OrderItem.objects.create(order=order1, product=products[0], quantity=2)
    OrderItem.objects.create(order=order1, product=products[1], quantity=1)
    order1.update_total()
    
    order2= Order.objects.create(customer=customers[2])
    
    OrderItem.objects.create(order=order2, product=products[3])
    order2.update_total()

    return [order1,order2]

@pytest.fixture
def payments(orders,customers,products):
    payments= Payments.objects.create(order=orders[2],amount=orders[2].total)
    return [payments]

@pytest.mark.django_db
class TestApi:
    def test_get_all_products(self, api_client, products):
        response=api_client.get("/api/products/")
        assert response.status_code==200
        for i,product in enumerate(response.data):
            assert product["price"]==products[i].price
            assert product["stock"]==products[i].stock
            assert product["name"]==products[i].name

    def test_get_product_by_id(self, api_client,products):
        id=products[1].id
        response=api_client.get(f"/api/products/{id}/")
        assert response.status_code==200
        assert response.data["name"]==products[1].name
        assert response.data["stock"]==products[1].stock
        assert response.data["price"]==products[1].price
        assert response.data["id"]==id
    
    def test_get_product_by_id_not_found_404(self, api_client, products):
        response=api_client.get("/api/products/99999/")
        assert response.status_code==404
        assert response.data["error"]=="Product not found."
    
    def test_get_all_customers(self,api_client,customers):
        response=api_client.get("/api/customers/")
        assert response.status_code==200
        for i,customer in enumerate(response.data):
            assert customer["name"]==customers[i].name
            assert customer["email"]==customers[i].email
            assert int(customer["phone"])==customers[i].phone
            
        

