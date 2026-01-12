from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ExpenseForm
from .models import Expense


@login_required
def expense_list(request):
    expenses = Expense.objects.filter(
        user=request.user
    ).select_related('category').order_by('-date')

    return render(
        request,
        'expenses/expense_list.html',
        {'expenses': expenses}
    )


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, user=request.user)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(user=request.user)

    return render(
        request,
        'expenses/add_expense.html',
        {'form': form}
    )
