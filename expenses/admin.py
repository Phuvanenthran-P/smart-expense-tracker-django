from django.contrib import admin
from .models import Category, Expense


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'monthly_limit', 'is_blocking')


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'amount', 'date')
    list_filter = ('category', 'payment_method')
