from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Product(models.Model):
    name = models.CharField(max_length=120, unique=True) # Title must be unique
    description = models.TextField(null=True, blank=True) 
    price = models.FloatField(validators=[MinValueValidator(1)]) # Price must be more than 0 (positive)
    created_by = models.ForeignKey( # Owner of the product
        User, on_delete=models.CASCADE, related_name="products"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.created_by.username}"
