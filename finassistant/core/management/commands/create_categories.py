from django.core.management.base import BaseCommand
from core.models import Category

class Command(BaseCommand):
    help = 'Створює базові категорії для фінансового менеджера'

    def handle(self, *args, **options):
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

        created_count = 0

        for cat_name in expense_categories:
            category, created = Category.objects.get_or_create(
                name=cat_name,
                type='expense',
                defaults={'owner': None}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Створено категорію витрат: {cat_name}')
                )
                created_count += 1
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠ Категорія витрат вже існує: {cat_name}')
                )

        for cat_name in income_categories:
            category, created = Category.objects.get_or_create(
                name=cat_name,
                type='income',
                defaults={'owner': None}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Створено категорію доходів: {cat_name}')
                )
                created_count += 1
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠ Категорія доходів вже існує: {cat_name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n🎉 Завершено! Створено {created_count} нових категорій.')
        )
        
        self.stdout.write('\n📋 Всі доступні категорії:')
        for cat in Category.objects.all().order_by('type', 'name'):
            icon = '💸' if cat.type == 'expense' else '💰'
            self.stdout.write(f'  {icon} {cat.name} ({cat.get_type_display()})')
