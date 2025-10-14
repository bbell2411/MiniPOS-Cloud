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
def payments(orders):
    payments= Payments.objects.create(order=orders[1])
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

    def test_get_customer_by_id(self, api_client, customers):
        customer= customers[0]
        response=api_client.get(f"/api/customers/{customer.id}/")
        assert response.status_code==200
        assert response.data["name"]==customer.name
        assert int(response.data["phone"])==customer.phone
        assert response.data["email"]==customer.email
        
    def test_get_customer_by_id_not_found_404(self,api_client,customers):
        response= api_client.get("/api/customers/9999/")
        assert response.status_code==404
        assert response.data["error"]=="customer not found."

    def test_get_all_payments(self,api_client,payments):
        response=api_client.get("/api/payments/")
        assert response.status_code==200
        for i,payment in enumerate(response.data):
            assert payment["order"]==payments[i].order.id
            assert payment["amount"]==payments[i].amount
            assert payment["status"]==payments[i].status
    
    def test_get_payment_by_id(self,api_client,payments):
        payment=payments[0]
        response=api_client.get(f"/api/payments/{payment.id}/")
        assert response.status_code==200
        assert response.data["id"]==payment.id
        assert response.data["order"]==payment.order.id
        assert response.data["status"]==payment.status
        assert response.data["amount"]==payment.amount
        
    def test_get_payment_by_id_not_found_404(self,api_client,payments):
        response=api_client.get("/api/payments/9999/")
        assert response.status_code==404
        assert response.data["error"]=="Payment not found."
    
    def test_get_all_orders(self, api_client, orders):
        response=api_client.get("/api/orders/")
        assert response.status_code==200
        for i,order in enumerate(response.data):
            assert order["customer"]==orders[i].customer.id
            assert order["created_at"] == orders[i].created_at.isoformat().replace("+00:00", "Z")
            assert order["total"]==orders[i].total
            assert order["status"]==orders[i].status
            assert order["order_items"]==list(orders[i].order_items.values_list("id",flat=True))
            
        assert isinstance(order["order_items"], list)
        
    def test_get_order_by_id(self,api_client,orders):
        order=orders[1]
        response=api_client.get(f"/api/orders/{order.id}/")
        assert response.status_code==200
        assert response.data["customer"]==order.customer.id
        assert response.data["created_at"]==order.created_at.isoformat().replace("+00:00","Z")
        assert response.data["total"]==order.total
        assert response.data["status"]==order.status
        assert response.data["order_items"]==list(order.order_items.values_list("id",flat=True))
        assert response.data["id"]==order.id
    
    def test_get_order_by_id_not_found_404(self,api_client,orders):
        response=api_client.get("/api/orders/999/")
        assert response.status_code==404
        assert response.data["error"]=="Order not found."

    def test_get_order_items(self,api_client,orders):
        order=orders[0]
        response=api_client.get(f"/api/orders/{order.id}/items/")
        assert response.status_code==200
        items=order.items.all()
        for i,item in enumerate(response.data):
            assert item["id"]==items[i].id
            assert item["product"]==items[i].product.id  
            assert item["quantity"]==items[i].quantity    
            assert item["subtotal"]==items[i].subtotal
            assert item["order"]==items[i].order.id    
            
    def test_get_order_items_order_not_found_404(self,api_client,orders):
        response=api_client.get("/api/orders/9999/items/")
        assert response.status_code==404
        assert response.data["error"]=="Order not found."
                
    def test_get_order_items_by_id(self,api_client,orders):
        order=orders[0]
        item=order.items.all()[0]
        response=api_client.get(f"/api/orders/{order.id}/items/{item.id}/")
        assert response.status_code==200
        assert response.data["id"]==item.id
        assert response.data["order"]==item.order.id
        assert response.data["product"]==item.product.id
        assert response.data["quantity"]==item.quantity
        assert response.data["subtotal"]==item.subtotal
        
    def test_get_order_items_by_id_item_not_found_404(self,api_client,orders):
        order=orders[0]
        response=api_client.get(f"/api/orders/{order.id}/items/999/")
        assert response.status_code==404
        assert response.data["error"]=="Item not found."
        
    def test_post_customer(self,api_client,customers):
        payload={
            "name":"bell",
            "email":"bell@gmail.com"
        }
        response=api_client.post("/api/customers/",payload)
        assert response.status_code==201
        assert response.data["name"]==payload["name"]
        assert response.data["email"]==payload["email"]
        assert response.data["phone"] is None
        assert Customer.objects.count() == len(customers)+1
        
        new_customer=Customer.objects.last()
        assert new_customer.name==payload["name"]
        assert new_customer.email==payload["email"]
        
        
        
