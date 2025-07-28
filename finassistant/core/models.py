from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

class Category(models.Model):
    TYPE_CHOICES = (
        ('income', 'Дохід'),
        ('expense', 'Витрата'),
    )
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories', null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.amount} ({self.category})"

class Event(models.Model):
    PRIORITY_CHOICES = (
        ('low', 'Низький'),
        ('medium', 'Середній'),
        ('high', 'Високий'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default='medium')
    date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.date}"

    class Meta:
        ordering = ['-date']