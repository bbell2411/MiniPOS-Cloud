from pos.models import Customer, Product
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        products=[
            {"name":"coffee","price":250,"stock":100},
            {"name":"water","price":50,"stock":500},
            {"name":"matcha","price":600,"stock":70},
            {"name":"velvet cake","price":1000,"stock":50},
            {"name":"chocolate cake","price":700,"stock":100},
        ]
        
        for product in products:
            p,created=Product.objects.get_or_create(
                name=product["name"],
                price=product["price"],
                defaults={
                    "stock":product["stock"]
                }
            )
        if created:
            self.stdout.write(self.style.SUCCESS("Products table successfully seeded!"))
                
        self.stdout.write(self.style.SUCCESS("Products table already seeded!"))
     
        customers=[
            {"name":"patrick","email":"patrick@gmail.com","phone":987654321},
            {"name":"olivia","email":"olivia@gmail.com","phone":987654322},
            {"name":"josh","email":"josh@gmail.com","phone":987654323},
            ]
        for cust in customers:
            c,created=Customer.objects.get_or_create(
                name=cust["name"],
                email=cust["email"],
                phone=cust["phone"]
            )
        if created:
            self.stdout.write(self.style.SUCCESS("Customers table successfully seeded!"))
            
        self.stdout.write(self.style.SUCCESS("Customers table already seeded!"))
            
        