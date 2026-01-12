from django.db.models import Sum
from datetime import date

def evaluate_expense(category, amount):
    today = date.today()
    monthly_total = category.expense_set.filter(
        date__year=today.year,
        date__month=today.month
    ).aggregate(total=Sum('amount'))['total'] or 0

    projected_total = monthly_total + amount

    if category.monthly_limit:
        percentage = (projected_total / category.monthly_limit) * 100

        if percentage >= 100 and category.is_blocking:
            return "BLOCK", "Monthly limit exceeded"

        if percentage >= category.warning_threshold:
            return "WARN", "Approaching monthly limit"

    return "ALLOW", None
