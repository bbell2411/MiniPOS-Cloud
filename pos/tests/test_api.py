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
        
    def test_post_order_items(self,api_client,orders,products):
        order=orders[0]
        product=products[2]
        
        initial_count = OrderItem.objects.filter(order=order).count()
        
        payload={
            "order":order.id,
            "product":product.id,
            "quantity":5
        }
        response=api_client.post(f"/api/orders/{payload["order"]}/items/", payload, format="json")
        assert response.status_code==201
        assert response.data["order"]==payload["order"]
        assert response.data["product"]==payload["product"]
        assert response.data["quantity"]==payload["quantity"]
        assert response.data["subtotal"]== products[2].price*payload["quantity"]
        
        updated_order_items=OrderItem.objects.filter(order=order.id)
        assert updated_order_items.count()==initial_count+1
        
        assert updated_order_items.last().product.id==payload["product"]
        assert updated_order_items.last().quantity==payload["quantity"]
        assert updated_order_items.last().order.id==payload["order"]
        
    def test_post_order_items_not_found_404(self, api_client, orders, products):
        order=orders[0]
        product=products[2]
        payload={
            "order":order.id,
            "product":product.id,
            "quantity":5
        }
        response=api_client.post("/api/orders/8989/items/", payload, format="json")
        assert response.status_code==404
        assert response.data["error"]=="Order not found."
        
    def test_post_order_items_missing_data_400(self, api_client, orders, products):
        order=orders[0]
        product=products[2]
        payload={
            "order":order.id,
            "quantity":5
        }
        response=api_client.post(f"/api/orders/{payload["order"]}/items/", payload, format="json")
        assert response.status_code==400
        assert "product" in response.data

    def test_post_order_items_invalid_data_400(self, api_client, orders, products):
        order=orders[0]
        product=products[2]
        payload={
            "order":order.id,
            "product":product.id,
            "quantity":"string"
        }
        response=api_client.post(f"/api/orders/{payload["order"]}/items/", payload, format="json")
        assert response.status_code==400
        assert "quantity" in response.data
        
    def test_patch_order_item(self, api_client, orders, products):
        order=orders[0]
        product=products[2]
        post_payload={
            "order":order.id,
            "product":product.id,
            "quantity":69
        }
        post_response=api_client.post(f"/api/orders/{order.id}/items/", post_payload, format="json")
        assert post_response.status_code==201
        posted_order_item=OrderItem.objects.filter(order=order.id).last()
        
        patch_payload={
            "product":product.id,
        }
        product_price=Product.objects.get(id=product.id)
        patch_response=api_client.patch(f"/api/orders/{order.id}/items/{posted_order_item.id}/", patch_payload, format="json")
        assert patch_response.status_code==200
        assert patch_response.data["product"]==patch_payload["product"]
        assert patch_response.data["order"]==posted_order_item.order.id
        assert patch_response.data["subtotal"] == product_price.price * patch_response.data["quantity"]
        
    def test_patch_order_item_invalid_data_400(self, api_client, orders, products):
        order=orders[0]
        product=products[2]
        post_payload={
            "order":order.id,
            "product":product.id,
            "quantity":69
        }
        post_response=api_client.post(f"/api/orders/{order.id}/items/", post_payload, format="json")
        assert post_response.status_code==201
        posted_order_item=OrderItem.objects.filter(order=order.id).last()
        
        patch_payload={
            "product":"two",
        }
        response=api_client.patch(f"/api/orders/{order.id}/items/{posted_order_item.id}/",patch_payload, format="json")
        assert response.status_code==400
        assert "product" in response.data
        
    def test_patch_order_item_not_found_404(self, api_client, orders, products):
        order=orders[0]
        product=products[2]
        post_payload={
            "order":order.id,
            "product":product.id,
            "quantity":69
        }
        post_response=api_client.post(f"/api/orders/{order.id}/items/", post_payload, format="json")
        assert post_response.status_code==201
        
        patch_payload={
            "quantity":4
        }
        
        response=api_client.patch(f"/api/orders/{order.id}/items/897977/",patch_payload, format="json")
        assert response.status_code==404
        assert response.data["error"]=="Item not found."
        
    def test_patch_order_order_not_found_404(self, api_client, orders, products):
        order=orders[0]
        product=products[2]
        post_payload={
            "order":order.id,
            "product":product.id,
            "quantity":69
        }
        post_response=api_client.post(f"/api/orders/{order.id}/items/", post_payload, format="json")
        assert post_response.status_code==201
        posted_order_item=OrderItem.objects.filter(order=order.id).last()
        
        patch_payload={
            "quantity":4
        }
        response=api_client.patch(f"/api/orders/867688/items/{posted_order_item.id}/",patch_payload, format="json")
        assert response.status_code==404
        assert response.data["error"]=="Order not found."
        
    def test_patch_order_item_not_in_order_404(self,api_client,products, orders):
        order1=orders[0]
        order2=orders[1]
        product=products[0]
        payload={
            "order":order1.id,
            "product":product.id
        }
        post_response=api_client.post(f"/api/orders/{payload['order']}/items/",payload,format="json")
        assert post_response.status_code==201        
        posted_order_item=OrderItem.objects.filter(order=order1.id).last()
        patch_payload={
            "quantity":2
        }        
        response=api_client.patch(f'/api/orders/{order2.id}/items/{posted_order_item.id}/',patch_payload,format="json")
        assert response.status_code==404
        assert response.data["error"]=="Item not found in this order."
        
    def test_patch_order_item_empty_payload(self,api_client,orders, products):
        order=orders[0]
        product=products[0]
        post_payload={
            "order":order.id,
            "product":product.id
        }
        post_response=api_client.post(f"/api/orders/{post_payload['order']}/items/",post_payload, format="json")
        assert post_response.status_code==201
        posted_order_item=OrderItem.objects.filter(order=order).last()
        payload={}
        response=api_client.patch(f"/api/orders/{order.id}/items/{posted_order_item.id}/",payload, format="json")
        assert response.status_code==400
        assert response.data["error"]=="No data provided."
        
    def test_post_customer(self,api_client,customers):
        payload={
            "name":"bell",
            "email":"bell@gmail.com"
        }
        response=api_client.post("/api/customers/",payload, format="json")
        assert response.status_code==201
        assert response.data["name"]==payload["name"]
        assert response.data["email"]==payload["email"]
        assert response.data["phone"] is None
        assert Customer.objects.count() == len(customers)+1
        
        new_customer=Customer.objects.last()
        assert new_customer.name==payload["name"]
        assert new_customer.email==payload["email"]
        
        
    def test_post_customer_invalid_data_400(self,api_client,customers):
        payload={
            "name":" "
        }
        response=api_client.post("/api/customers/",payload)
        assert response.status_code==400
        assert "name" in response.data
        
    def test_post_customer_missing_data_400(self,api_client,customers):
        payload={
            "phone":87272672
        }
        response=api_client.post("/api/customers/",payload)
        assert response.status_code==400
        assert "name" in response.data
        
    def test_post_customer_missing_data_400(self,api_client,customers):
        payload={
            "phone":"not a number",
            "name":"bell"
        }
        response=api_client.post("/api/customers/",payload)
        assert response.status_code==400
        assert "phone" in response.data
        
    def test_patch_customer(self, api_client, customers):
        payload={
            "email":"newEmail@gmai.com"
        }
        customer=customers[1]
        response=api_client.patch(f"/api/customers/{customer.id}/",payload, format="json")
        assert response.status_code==200
        customer.refresh_from_db()
        assert customer.email==payload["email"]
    
    def test_patch_customer_not_found_404(self,api_client,customers):
        payload={
            "email":"newEmail@gmai.com"
        }
        response=api_client.patch("/api/customers/676877/",payload,format="json")
        assert response.status_code==404
        assert response.data["error"]=="Customer not found."
        
    def test_patch_customer_no_change_200(self,api_client,customers):
        payload={
        }
        customer=customers[1]
        response=api_client.patch(f"/api/customers/{customer.id}/",payload, format="json")
        assert response.status_code==200
        customer.refresh_from_db()
        assert response.data["name"]==customer.name
        assert response.data["email"]==customer.email        
        assert response.data["phone"]==customer.phone  
    
    def test_patch_customer_invalid_data_400(self,api_client,customers):
        payload={
            "phone":"newEmail@gmai.com"
        }
        customer=customers[1]
        response=api_client.patch(f"/api/customers/{customer.id}/",payload, format="json")
        assert response.status_code==400
        assert "phone" in response.data
    
    def test_delete_customer(self,api_client,customers):
        #only admins (implementation later)
        customer=customers[0]
        response=api_client.delete(f"/api/customers/{customer.id}/")
        assert response.status_code==204
        assert Customer.objects.count()==len(customers)-1

    def test_delete_customer_not_found_404(self,api_client,customers):
        response=api_client.delete("/api/customers/6747/")
        assert response.status_code==404
        assert response.data["error"]=="Customer not found."
        
    def test_post_order(self,api_client,orders,customers):
        #again only admin/employees laterrrr
        customer=customers[1]
        payload={
            "customer":customer.id,
            }
        response=api_client.post("/api/orders/", payload,format="json")
        assert response.status_code==201
        assert response.data["customer"]==payload["customer"]
        assert "created_at" in response.data
        assert response.data["total"]==0
        assert response.data["status"].lower()=="pending"
        assert len(response.data["order_items"])==0
        assert Order.objects.count()==len(orders)+1
        
    def test_post_order_missing_data_400(self,api_client,orders):
        payload={}
        response=api_client.post("/api/orders/",payload,format="json")
        assert response.status_code==400
        assert "customer" in response.data
    
    def test_post_order_invalid_data_400(self,api_client,orders):
        payload={"customer":"hey"}
        response=api_client.post("/api/orders/",payload,format="json")
        assert response.status_code==400
        assert "customer" in response.data
        