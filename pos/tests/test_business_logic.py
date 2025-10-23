import pytest
from rest_framework.test import APIClient
from pos.models import Product,Customer, Order, Payments, OrderItem

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
    
    OrderItem.objects.create(order=order1, product=products[0], quantity=2)
    OrderItem.objects.create(order=order1, product=products[1], quantity=1)
    order1.update_total()
    
    order2= Order.objects.create(customer=customers[2])
    
    OrderItem.objects.create(order=order2, product=products[3])
    order2.update_total()

    return [order1,order2]

@pytest.fixture
def order1_items(orders):
    order1 = orders[0]
    return OrderItem.objects.filter(order=order1)

@pytest.fixture
def payments(orders):
    payments= Payments.objects.create(order=orders[1])
    return [payments]

@pytest.mark.django_db
class TestBusinesslogic:
    def test_update_totals_add_remove_items(self, orders, products):
        order= orders[0]
        assert order.total==400
        
        new_product=products[2]
        item=OrderItem.objects.create(order=order, product=new_product)
        order.update_total()
        order.refresh_from_db()
        assert order.total==650
        
        item.delete()
        order.refresh_from_db()
        assert order.total==650
        
        order.update_total()
        order.refresh_from_db()
        assert order.total==400
    
    def test_update_totals_quantity_change(self, orders):
        order= orders[0]
        assert order.total==400
        
        items= order.items.all()
        item = items.first()
        
        item.quantity = 10
        item.save()
        order.refresh_from_db()
        
        assert order.total==1200
        
    def test_quantity_zero_raises_error(self, order1_items):
        item= order1_items[0]
        
        with pytest.raises(ValueError, match="Quantity must be at least 1"):
            item.quantity=0
            item.save()
            
    def test_quantity_quantity_exceeds_stock_raise_error(self, order1_items, products):
        item= order1_items[0]
            
        with pytest.raises(ValueError, match="Not enough stock"):
            item.quantity = products[0].stock + 1
            item.save()
            
         # create payment mock gateway 
         # and make payment intent
         # make sure to test and make test 
         # make sure for updated_at and status management
         #create payment intent table storing all intents????? idk
         # post order to payment and if sucessful then mark status as completed in both
         # err handle