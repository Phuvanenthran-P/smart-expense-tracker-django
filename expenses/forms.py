from django import forms
from .models import Expense, Category
from .services import evaluate_expense


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'date', 'payment_method', 'note']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user:
            self.fields['category'].queryset = Category.objects.filter(
                user=self.user
            )

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is None or amount <= 0:
            raise forms.ValidationError("Amount must be positive")
        return amount

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        amount = cleaned_data.get('amount')

        if not self.user:
            raise forms.ValidationError("User context missing")

        if category and category.user != self.user:
            raise forms.ValidationError("Invalid category selection")

        if category and amount:
            decision, message = evaluate_expense(
                category=category,
                amount=amount,
                user=self.user
            )

            if decision == "BLOCK":
                raise forms.ValidationError(message)

            if decision == "WARN":
                self.add_error(None, message)

        return cleaned_data
