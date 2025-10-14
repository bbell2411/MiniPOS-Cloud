from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    name=models.CharField(max_length=100, null=False, blank=False)
    email=models.EmailField(unique=True, null=True, blank=True)
    phone=models.IntegerField(max_length=15, unique=True, null=True, blank=True)
     
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.IntegerField()
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.IntegerField(default=0)
    order_items = models.ManyToManyField(Product, through='OrderItem')
    status = models.CharField(max_length=20, choices=[('Pending', 'pending'), ('Completed', 'completed'), ('Cancelled', 'cancelled')], default='Pending')
    
    def update_total(self):
        total = sum(item.subtotal for item in self.items.all())
        self.total = total
        self.save()
    
    def __str__(self):
        return f"Order {self.id}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        self.subtotal = self.product.price * self.quantity
        super().save(*args, **kwargs)
        self.order.refresh_from_db()
        self.order.update_total()
        
class Payments(models.Model):
    order=models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    amount=models.PositiveIntegerField()
    status=models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.amount:
            self.amount = self.order.total
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment for Order {self.order.id} - {self.status}"
    