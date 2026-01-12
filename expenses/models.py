from django.db import models
from django.conf import settings


class Category(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='categories'
    )
    name = models.CharField(max_length=100)
    monthly_limit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    warning_threshold = models.PositiveIntegerField(default=80)
    is_blocking = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Expense(models.Model):
    PAYMENT_CHOICES = [
        ('CASH', 'Cash'),
        ('CARD', 'Card'),
        ('UPI', 'UPI'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='expenses'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='expenses'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category.name} - {self.amount}"
