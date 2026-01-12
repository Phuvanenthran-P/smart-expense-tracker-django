from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'date', 'payment_method', 'note']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError("Amount must be positive")
        return amount

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        amount = cleaned_data.get('amount')

        if category and amount:
            decision, message = evaluate_expense(category, amount)
            if decision == "BLOCK":
                raise forms.ValidationError(message)
            if decision == "WARN":
                self.add_error(None, message)

        return cleaned_data
