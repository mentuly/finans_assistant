import pytest
from datetime import date, timedelta
from core.forms import CategoryForm, TransactionForm, EventForm


@pytest.mark.django_db
class TestCategoryForm:
    
    def test_valid_category_form(self):
        form_data = {'name': 'Їжа', 'type': 'expense'}
        form = CategoryForm(data=form_data)
        assert form.is_valid()


@pytest.mark.django_db  
class TestTransactionForm:
    
    def test_valid_transaction_form(self, user_factory):
        user = user_factory()
        form_data = {
            'category_choice': 'Їжа',
            'amount': '150.50',
            'description': 'Обід'
        }
        form = TransactionForm(user=user, data=form_data)
        assert form.is_valid()


@pytest.mark.django_db
class TestEventForm:
    
    def test_valid_event_form(self):
        future_date = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        form_data = {
            'title': 'Тестова подія',
            'date': future_date,
            'priority': 'medium'
        }
        form = EventForm(data=form_data)
        assert form.is_valid()