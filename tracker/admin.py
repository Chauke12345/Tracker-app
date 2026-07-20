from django.contrib import admin
from .models import Expense, BankStatement


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("title", "amount", "type", "category", "date")


@admin.register(BankStatement)
class BankStatementAdmin(admin.ModelAdmin):
    list_display = ("user", "file", "uploaded_at")