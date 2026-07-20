from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Expense, BankStatement


# 💰 Expense Form
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["title", "amount", "type", "category"]


# 🔐 Signup Form
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


# 📄 Bank Statement Upload Form
class BankStatementForm(forms.ModelForm):
    class Meta:
        model = BankStatement
        fields = ["file"]