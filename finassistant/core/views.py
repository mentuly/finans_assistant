from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from datetime import datetime, timedelta
import json
from .forms import TransactionForm, EventForm
from .models import Transaction, Category, Event

@login_required
def dashboard(request):
    user_transactions = Transaction.objects.filter(user=request.user)
    income = user_transactions.filter(category__type='income').aggregate(total=Sum('amount'))['total'] or 0
    expenses = user_transactions.filter(category__type='expense').aggregate(total=Sum('amount'))['total'] or 0
    balance = income - expenses
    today = datetime.now()
    months = []
    monthly_income = []
    monthly_expenses = []
    
    for i in range(2, -1, -1):
        month_start = today.replace(day=1) - timedelta(days=30*i)
        month_end = month_start + timedelta(days=31)
        
        month_income = user_transactions.filter(
            category__type='income',
            date__gte=month_start.date(),
            date__lt=month_end.date()
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        month_expenses = user_transactions.filter(
            category__type='expense',
            date__gte=month_start.date(),
            date__lt=month_end.date()
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        months.append(month_start.strftime('%B'))
        monthly_income.append(float(month_income))
        monthly_expenses.append(float(month_expenses))
    
    context = {
        "balance": balance,
        "income": income,
        "expenses": expenses,
        "events_count": Event.objects.filter(user=request.user).count(),
        "chart_labels": json.dumps(months),
        "chart_income": json.dumps(monthly_income),
        "chart_expenses": json.dumps(monthly_expenses),
    }
    return render(request, "dashboard.html", context)

@login_required
def profile(request):
    if request.method == 'POST' and request.FILES.get('avatar'):
        request.user.avatar = request.FILES['avatar']
        request.user.save()
        return redirect('profile')
    return render(request, "profile.html")

@login_required
def events(request):
    events = Event.objects.filter(user=request.user).order_by('-date')
    return render(request, "events.html", {"events": events})

@login_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, user=request.user)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            
            category_choice = form.cleaned_data.get('category_choice')
            new_category_name = form.cleaned_data.get('new_category')
            
            if category_choice:
                category_type = 'income' if event.amount and event.amount > 0 else 'expense'
                category, created = Category.objects.get_or_create(
                    name=category_choice,
                    type=category_type,
                    defaults={'owner': request.user}
                )
                event.category = category
            elif new_category_name:
                category_type = 'income' if event.amount and event.amount > 0 else 'expense'
                category, created = Category.objects.get_or_create(
                    name=new_category_name,
                    type=category_type,
                    defaults={'owner': request.user}
                )
                event.category = category
            
            event.save()
            messages.success(request, f'Подію "{event.title}" успішно додано!')
            return redirect('events')
    else:
        form = EventForm(user=request.user)
    return render(request, 'add_event.html', {'form': form})

@login_required
def toggle_event(request, event_id):
    event = Event.objects.get(id=event_id, user=request.user)
    event.completed = not event.completed
    event.save()
    return redirect('events')

@login_required
def add_transaction(request, type):
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user, transaction_type=type)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            
            category_choice = form.cleaned_data.get('category_choice')
            new_category_name = form.cleaned_data.get('new_category')
            
            if category_choice:
                category, created = Category.objects.get_or_create(
                    name=category_choice,
                    type=type,
                    defaults={'owner': request.user}
                )
                transaction.category = category
            elif new_category_name:
                category, created = Category.objects.get_or_create(
                    name=new_category_name,
                    type=type,
                    defaults={'owner': request.user}
                )
                transaction.category = category
            else:
                form.add_error('new_category', 'Оберіть категорію зі списку або введіть нову')
                return render(request, 'add_transaction.html', {
                    'form': form,
                    'type': type,
                })
            
            transaction.save()
            messages.success(request, f'Транзакцію успішно додано!')
            return redirect('transactions')
    else:
        form = TransactionForm(user=request.user, transaction_type=type)
    
    return render(request, 'add_transaction.html', {
        'form': form,
        'type': type,
    })

@login_required
def transactions(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, "transactions.html", {
        "transactions": transactions,
    })