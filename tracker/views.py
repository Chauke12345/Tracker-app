from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout

import json

from .models import Expense
from .forms import ExpenseForm, SignUpForm
from django.utils import timezone
from django.db.models.functions import TruncMonth
from django.db.models import Q





# ---------------------------------------------------
# 📊 DASHBOARD / HOME PAGE
# ---------------------------------------------------

@login_required(login_url="/login/")
def expense_list(request):

    today = timezone.now()

    expenses = Expense.objects.filter(
        user=request.user,
        date__year=today.year,
        date__month=today.month
    ).order_by("-date")

    income = sum(e.amount for e in expenses if e.type == "income")
    expense = sum(e.amount for e in expenses if e.type == "expense")
    balance = income - expense

    monthly_data = (
        Expense.objects
        .filter(user=request.user)
        .annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(
            income=Sum("amount", filter=Q(type="income")),
            expense=Sum("amount", filter=Q(type="expense"))
        )
        .order_by("month")
    )
    # ---------------------------------------------------
    # 📊 MONTHLY CHART DATA (income + expense properly)
    # ---------------------------------------------------
   

    months = []
    income_data = []
    expense_data = []
    balance_data = []

    for item in monthly_data:
        inc = item["income"] or 0
        exp = item["expense"] or 0

        months.append(item["month"].strftime("%Y-%m"))
        income_data.append(float(inc))
        expense_data.append(float(exp))
        balance_data.append(float(inc - exp))

    context = {
        "expenses": expenses,
        "income": income,
        "expense": expense,
        "balance": balance,

        # chart data
        "months_json": json.dumps(months),
        "income_json": json.dumps(income_data),
        "expense_json": json.dumps(expense_data),
        "balance_json": json.dumps(balance_data),
    }

    return render(request, "tracker/index.html", context)
# ---------------------------------------------------
# ➕ ADD EXPENSE (LOGIN REQUIRED)
# ---------------------------------------------------
@login_required(login_url="/login/")
def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)  # don't save yet
            expense.user = request.user        # link to logged-in user
            expense.save()
            return redirect("home")
    else:
        form = ExpenseForm()

    return render(request, "tracker/add_expense.html", {"form": form})


# ---------------------------------------------------
# ✏️ EDIT EXPENSE
# ---------------------------------------------------
@login_required(login_url="/login/")
def edit_expense(request, id):
    expense_obj = get_object_or_404(
        Expense,
        id=id,
        user=request.user
    )

    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense_obj)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = ExpenseForm(instance=expense_obj)

    return render(request, "tracker/edit_expense.html", {"form": form})


# ---------------------------------------------------
# 🗑 DELETE EXPENSE
# ---------------------------------------------------
@login_required(login_url="/login/")
def delete_expense(request, id):
    expense_obj = get_object_or_404(
        Expense,
        id=id,
        user=request.user
    )

    if request.method == "POST":
        expense_obj.delete()
        return redirect("home")

    return render(request, "tracker/delete_confirm.html", {"expense": expense_obj})


# ---------------------------------------------------
# 🧾 SIGNUP PAGE
# ---------------------------------------------------
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)   # auto-login after signup
            return redirect("home")
    else:
        form = SignUpForm()

    return render(request, "tracker/signup.html", {"form": form})


# ---------------------------------------------------
# 🔐 LOGIN VIEW (class-based)
# ---------------------------------------------------
class CustomLoginView(LoginView):
    template_name = "tracker/login.html"
    redirect_authenticated_user = True


# ---------------------------------------------------
# 🚪 LOGOUT VIEW
# ---------------------------------------------------
def logout_view(request):
    logout(request)
    return redirect("login")

