from django.db import models
from django.contrib.auth.models import User


class Expense(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    CATEGORY_CHOICES = [
        ("salary", "Salary"),
        ("freelance", "Freelance"),
        ("investment", "Investment"),

        ("groceries", "Groceries"),
        ("food", "Food & Dining"),
        ("transport", "Transport"),
        ("fuel", "Fuel"),
        ("rent", "Rent"),
        ("utilities", "Utilities"),
        ("shopping", "Shopping"),
        ("entertainment", "Entertainment"),
        ("healthcare", "Healthcare"),
        ("education", "Education"),
        ("insurance", "Insurance"),
        ("travel", "Travel"),
        ("subscriptions", "Subscriptions"),
        ("savings", "Savings"),
        ("other", "Other"),
    ]


    TYPE_CHOICES = [
        ("income", "Income"),
        ("expense", "Expense"),
    ]


    title = models.CharField(
        max_length=200
    )


    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )


    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )


    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES
    )


    date = models.DateField()


    def __str__(self):
        return f"{self.title} - {self.amount}"


    class Meta:
        ordering = ["-date"]



class BankStatement(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bank_statements"
    )


    file = models.FileField(
        upload_to="bank_statements/"
    )


    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return f"{self.user.username} - {self.uploaded_at.date()}"