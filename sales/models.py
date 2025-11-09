from django.db import models
from django.utils import timezone

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('drink', 'Drink'),
        ('snack', 'Snack'),
        ('other', 'Other'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.category}"

class SaleTransaction(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Transaction #{self.id} - {self.timestamp.strftime('%y-%m-%d %H:%M')}"


class SaleItem(models.Model):
            transaction = models.ForeignKey(SaleTransaction, on_delete=models.CASCADE, related_name='items')
            product = models.ForeignKey(Product, on_delete=models.CASCADE)
            quantity = models.PositiveIntegerField()
            subtotal = models.DecimalField(max_digits=10, decimal_places=2)

            def save(self, *args, **kwargs):
                #Automatically calculate subtotal
                self.subtotal = self.product.price * self.quantity
                super().save(*args, **kwargs)
                #Update total amount on parent transaction
                self.transaction.total_amount = sum(item.subtotal for item in self.transaction.items.all())
                self.transaction.save()

            def __str__(self):
                return f"{self.product.name} x{self.quantity}"

