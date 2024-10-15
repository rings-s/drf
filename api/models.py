import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.



class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True, help_text=("User's phone number."))
    birth_date = models.DateField(blank=True, null=True, help_text=("User's date of birth."))
    profile_photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, null=True, help_text=("User's profile photo."))

    # Additional field examples
    bio = models.TextField(("bio"), max_length=500, blank=True, help_text=("Short biography of the user"))
    
    def __str__(self):
        return self.username




class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    
    
    @property
    def in_stock(self):
        return self.stock > 0
    
    def __str__(self):
        return self.name
    

class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRM = 'confirm', 'Confirm'
        CANCELLED = 'cancelled', 'Cancelled'
        SHIPPED = 'shipped', 'Shipped'
        DELIVERED = 'delivered', 'Delivered'
        
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    
    products = models.ManyToManyField(Product, through='OrderItem', related_name='orders')
    
    def __str__(self):
        return f"order {self.order_id} by {self.user.username}"
    


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
    @property
    def item_subtotal(self):
        return self.quantity * self.product.price
    
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name} in order {self.order.order_id}"
    
    