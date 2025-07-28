import os
import sys
import django


sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finassistant.settings')
django.setup()

from core.models import Category

expense_categories = [
    'Їжа',
    'Транспорт', 
    'Покупки',
    'Інше'
]

income_categories = [
    'Зарплата',
    'Інше'
]

for name in expense_categories:
    category, created = Category.objects.get_or_create(
        name=name,
        type='expense',
        owner=None
    )
    if created:
        print(f"Створено категорію витрат: {name}")
    else:
        print(f"Категорія витрат вже існує: {name}")

for name in income_categories:
    category, created = Category.objects.get_or_create(
        name=name,
        type='income',
        owner=None
    )
    if created:
        print(f"Створено категорію доходів: {name}")
    else:
        print(f"Категорія доходів вже існує: {name}")

print("Готово! Всі категорії створені.")
