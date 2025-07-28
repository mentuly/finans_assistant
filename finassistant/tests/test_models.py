import pytest
from decimal import Decimal
from datetime import date, timedelta
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from core.models import User, Category, Transaction, Event


@pytest.mark.django_db
class TestUserModel:
    
    def test_user_creation(self, user_factory):
        user = user_factory(username='testuser', email='test@example.com')
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.check_password('testpass123')


@pytest.mark.django_db
class TestCategoryModel:
    
    def test_category_creation(self, user_factory, category_factory):
        user = user_factory()
        category = category_factory(name='Їжа', cat_type='expense', owner=user)
        
        assert category.name == 'Їжа'
        assert category.type == 'expense'
        assert category.owner == user
    
    def test_category_str_method(self, category_factory):
        category = category_factory(name='Їжа', cat_type='expense')
        assert str(category) == 'Їжа (Витрата)'


@pytest.mark.django_db
class TestTransactionModel:

    def test_transaction_creation(self, user_factory, category_factory, transaction_factory):
        user = user_factory()
        category = category_factory(name='Їжа', cat_type='expense')
        transaction = transaction_factory(
            user=user, 
            category=category, 
            amount='100.50',
            description='Обід в ресторані'
        )
        
        assert transaction.user == user
        assert transaction.category == category
        assert transaction.amount == Decimal('100.50')
        assert transaction.description == 'Обід в ресторані'
        assert transaction.date == date.today()
    
    def test_transaction_str_method(self, user_factory, category_factory, transaction_factory):
        user = user_factory()
        category = category_factory(name='Їжа', cat_type='expense')
        transaction = transaction_factory(user=user, category=category, amount='100.50')
        
        expected = f"100.50 ({category})"
        assert str(transaction) == expected


@pytest.mark.django_db
class TestEventModel:

    def test_event_creation(self, user_factory, category_factory):
        user = user_factory()
        category = category_factory(name='Зарплата', cat_type='income')
        
        event = Event.objects.create(
            user=user,
            title='Отримання зарплати',
            amount=Decimal('30000.00'),
            category=category,
            priority='high',
            date=date.today() + timedelta(days=5)
        )
        
        assert event.user == user
        assert event.title == 'Отримання зарплати'
        assert event.amount == Decimal('30000.00')
        assert event.priority == 'high'
        assert not event.completed


@pytest.mark.django_db
class TestBasicQueries:

    def test_income_expense_filtering(self, user_factory, category_factory, transaction_factory):
        user = user_factory()
        income_category = category_factory(name='Зарплата', cat_type='income')
        expense_category = category_factory(name='Їжа', cat_type='expense')
        
        transaction_factory(user=user, category=income_category, amount='30000.00')
        transaction_factory(user=user, category=expense_category, amount='5000.00')
        
        income_transactions = Transaction.objects.filter(user=user, category__type='income')
        expense_transactions = Transaction.objects.filter(user=user, category__type='expense')
        
        assert income_transactions.count() == 1
        assert expense_transactions.count() == 1
        assert income_transactions.first().amount == Decimal('30000.00')
        assert expense_transactions.first().amount == Decimal('5000.00')
