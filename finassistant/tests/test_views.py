import pytest
from decimal import Decimal
from django.test import Client
from django.urls import reverse
from core.models import Transaction, Event


@pytest.mark.django_db
class TestAuthentication:
    
    def test_dashboard_requires_login(self):
        client = Client()
        response = client.get(reverse('dashboard'))
        assert response.status_code == 302
        assert '/accounts/login/' in response.url


@pytest.mark.django_db
class TestDashboard:
    
    def test_dashboard_context(self, authenticated_client, transaction_factory, category_factory):
        income_cat = category_factory(name='Зарплата', cat_type='income')
        expense_cat = category_factory(name='Їжа', cat_type='expense')
        
        transaction_factory(user=authenticated_client.user, category=income_cat, amount='30000')
        transaction_factory(user=authenticated_client.user, category=expense_cat, amount='5000')
        
        response = authenticated_client.get(reverse('dashboard'))
        
        assert response.status_code == 200


@pytest.mark.django_db
class TestTransactions:
    
    def test_add_transaction_post_valid(self, authenticated_client):
        form_data = {
            'category_choice': 'Їжа',
            'amount': '150.50',
            'description': 'Обід'
        }
        response = authenticated_client.post(reverse('add_transaction', kwargs={'type': 'expense'}), data=form_data)
        assert response.status_code == 302
        
        transaction = Transaction.objects.filter(user=authenticated_client.user).first()
        assert transaction.amount == Decimal('150.50')