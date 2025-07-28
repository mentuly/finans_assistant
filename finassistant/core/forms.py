from django import forms
from .models import Transaction, Category, Event

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Назва категорії (наприклад: Кафе, Бензин, Подарунки)'
            }),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }

class TransactionForm(forms.ModelForm):
    CATEGORY_CHOICES = [
        ('', 'Оберіть категорію'),
        ('expense', [
            ('Їжа', 'Їжа'),
            ('Транспорт', 'Транспорт'),
            ('Покупки', 'Покупки'),
            ('Розваги', 'Розваги'),
            ('Комунальні', 'Комунальні послуги'),
            ('Здоров\'я', 'Здоров\'я'),
            ('Одяг', 'Одяг'),
            ('Інше_витрати', 'Інше'),
        ]),
        ('income', [
            ('Зарплата', 'Зарплата'),
            ('Фріланс', 'Фріланс'),
            ('Бонус', 'Бонус'),
            ('Подарунки', 'Подарунки'),
            ('Інше_доходи', 'Інше'),
        ]),
    ]
    
    category_choice = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control mb-2',
            'id': 'category-select'
        }),
        label='Швидкий вибір категорії'
    )
    
    new_category = forms.CharField(
        max_length=50, 
        required=False, 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Або введіть свою категорію'
        }),
        label='Власна категорія'
    )
    
    class Meta:
        model = Transaction
        fields = ['amount', 'category', 'description']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        self.transaction_type = kwargs.pop('transaction_type', None)
        super().__init__(*args, **kwargs)
        
        if self.transaction_type:
            self.fields['category'].queryset = Category.objects.filter(
                type=self.transaction_type, 
                owner__in=[user, None]
            )
            filtered_choices = [('', 'Оберіть категорію')]
            for group_name, choices in self.CATEGORY_CHOICES:
                if group_name == self.transaction_type:
                    filtered_choices.extend(choices)
            self.fields['category_choice'].choices = filtered_choices
        else:
            self.fields['category'].queryset = Category.objects.filter(owner__in=[user, None])
            
        self.fields['category'].required = False
        self.fields['amount'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Сума'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Опис'})
        self.fields['category'].empty_label = "Або оберіть існуючу"

class EventForm(forms.ModelForm):
    CATEGORY_CHOICES = [
        ('', 'Оберіть категорію'),
        ('Їжа', 'Їжа'),
        ('Транспорт', 'Транспорт'),
        ('Покупки', 'Покупки'),
        ('Розваги', 'Розваги'),
        ('Зарплата', 'Зарплата'),
        ('Фріланс', 'Фріланс'),
        ('Подарунки', 'Подарунки'),
        ('Інше', 'Інше'),
    ]
    
    category_choice = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control mb-2'
        }),
        label='Швидкий вибір категорії'
    )
    
    new_category = forms.CharField(
        max_length=50, 
        required=False, 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Або введіть свою категорію'
        }),
        label='Власна категорія'
    )
    
    class Meta:
        model = Event
        fields = ['title', 'description', 'amount', 'category', 'priority', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва події'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Опис події'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Сума (необов\'язково)'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(owner__in=[user, None])
            self.fields['category'].required = False
            self.fields['category'].empty_label = "Або оберіть існуючу"