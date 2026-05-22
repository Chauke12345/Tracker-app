from django import forms
from .models import Expense

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# 💰 Expense Form (your app core feature)
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'type', 'category']

# 🔐 Signup Form (authentication)
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]