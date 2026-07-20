import json
import csv
import pdfplumber

from datetime import datetime

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView

from django.db.models import Sum, Q
from django.db.models.functions import TruncMonth
from django.utils import timezone

from .models import Expense
from .forms import ExpenseForm, SignUpForm
# ---------------------------------------------------
# 📊 DASHBOARD / HOME PAGE
# ---------------------------------------------------

@login_required(login_url="/login/")
def expense_list(request):

    today = timezone.now()

    upload_message = None
    imported_count = 0

    # ---------------------------------------------------
    # 📄 BANK STATEMENT UPLOAD (CSV + PDF)
    # ---------------------------------------------------

    if request.method == "POST":

        uploaded_file = request.FILES.get("statement_file")

        if uploaded_file:

            filename = uploaded_file.name.lower()

            # ---------------------------------------
            # CSV IMPORT
            # ---------------------------------------

            if filename.endswith(".csv"):

                try:

                    decoded_file = (
                        uploaded_file
                        .read()
                        .decode("utf-8")
                        .splitlines()
                    )

                    reader = csv.DictReader(decoded_file)

                    for row in reader:

                        amount = float(
                            row.get("Amount", "0")
                            .replace("R", "")
                            .replace(",", "")
                            .strip()
                        )

                        if amount >= 0:
                            transaction_type = "income"
                            category = "salary"
                        else:
                            transaction_type = "expense"
                            category = "other"

                        transaction_date = datetime.strptime(
                            row.get("Date"),
                            "%Y-%m-%d"
                        ).date()

                        transaction_title = row.get(
                            "Description",
                            "Imported Transaction"
                        )

                        exists = Expense.objects.filter(
                            user=request.user,
                            title=transaction_title,
                            amount=abs(amount),
                            date=transaction_date,
                        ).exists()

                        if not exists:

                            Expense.objects.create(
                                user=request.user,
                                title=transaction_title,
                                amount=abs(amount),
                                category=category,
                                type=transaction_type,
                                date=transaction_date,
                            )

                            imported_count += 1

                    upload_message = (
                        f"✅ Imported {imported_count} new transactions. "
                        "Duplicate transactions were skipped."
                    )

                except Exception as e:

                    upload_message = (
                        f"❌ CSV Import failed: {str(e)}"
                    )

            # ---------------------------------------
            # PDF IMPORT
            # ---------------------------------------

            elif filename.endswith(".pdf"):

                try:

                    with pdfplumber.open(uploaded_file) as pdf:

                        for page in pdf.pages:

                            text = page.extract_text()

                            if text:

                                lines = text.split("\n")

                                for line in lines:

                                    parts = line.split()

                                    if len(parts) >= 3:

                                        try:

                                            transaction_date = datetime.strptime(
                                                parts[0],
                                                "%d-%m-%Y"
                                            ).date()

                                            amount = float(
                                                parts[-1]
                                                .replace(",", "")
                                            )

                                            description = " ".join(
                                                parts[1:-1]
                                            )

                                            if amount >= 0:
                                                transaction_type = "income"
                                                category = "salary"
                                            else:
                                                transaction_type = "expense"
                                                category = "other"

                                            exists = Expense.objects.filter(
                                                user=request.user,
                                                title=description,
                                                amount=abs(amount),
                                                date=transaction_date,
                                            ).exists()

                                            if not exists:

                                                Expense.objects.create(
                                                    user=request.user,
                                                    title=description,
                                                    amount=abs(amount),
                                                    category=category,
                                                    type=transaction_type,
                                                    date=transaction_date,
                                                )

                                                imported_count += 1

                                        except ValueError:
                                            continue

                    upload_message = (
                        f"✅ Imported {imported_count} new transactions. "
                        "Duplicate transactions were skipped."
                    )

                except Exception as e:

                    upload_message = (
                        f"❌ PDF Import failed: {str(e)}"
                    )

            else:

                upload_message = (
                    "❌ Only CSV and PDF files are supported"
                )

        else:

            upload_message = (
                "❌ No file uploaded"
            )

    # ---------------------------------------------------
    # 🧾 CURRENT MONTH TRANSACTIONS
    # ---------------------------------------------------

    expenses = Expense.objects.filter(
        user=request.user,
        date__year=today.year,
        date__month=today.month,
    ).order_by("-date")

    # ---------------------------------------------------
    # 💰 DASHBOARD TOTALS
    # ---------------------------------------------------

    income = sum(
        e.amount for e in expenses
        if e.type == "income"
    )

    expense = sum(
        e.amount for e in expenses
        if e.type == "expense"
    )

    balance = income - expense

    # ---------------------------------------------------
    # 📊 ADVANCED ANALYTICS
    # ---------------------------------------------------

    total_transactions = expenses.count()

    if income > 0:
        savings_rate = round(
            (balance / income) * 100,
            2
        )
    else:
        savings_rate = 0

    largest_expense = expenses.filter(
        type="expense"
    ).order_by(
        "-amount"
    ).first()

    average_expense = 0

    if total_transactions > 0:
        average_expense = round(
            expense / total_transactions,
            2
        )

    # ---------------------------------------------------
    # 📊 MONTHLY CHART DATA
    # ---------------------------------------------------

    monthly_data = (
        Expense.objects
        .filter(user=request.user)
        .annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(
            income=Sum(
                "amount",
                filter=Q(type="income")
            ),
            expense=Sum(
                "amount",
                filter=Q(type="expense")
            ),
        )
        .order_by("month")
    )

    months = []
    income_data = []
    expense_data = []
    balance_data = []

    for item in monthly_data:

        inc = item["income"] or 0
        exp = item["expense"] or 0

        months.append(
            item["month"].strftime("%Y-%m")
        )

        income_data.append(float(inc))
        expense_data.append(float(exp))
        balance_data.append(float(inc - exp))

    # ---------------------------------------------------
    # 📦 SEND DATA TO TEMPLATE
    # ---------------------------------------------------

    context = {

        # 📊 Advanced Analytics
        "total_transactions": total_transactions,
        "savings_rate": savings_rate,
        "largest_expense": largest_expense,
        "average_expense": average_expense,

        # 💰 Dashboard Totals
        "expenses": expenses,
        "income": income,
        "expense": expense,
        "balance": balance,

        # 📄 Upload Status
        "upload_message": upload_message,

        # 📊 Charts
        "months_json": json.dumps(months),
        "income_json": json.dumps(income_data),
        "expense_json": json.dumps(expense_data),
        "balance_json": json.dumps(balance_data),
    }

    return render(
        request,
        "tracker/index.html",
        context,
    )
# ---------------------------------------------------
# ➕ ADD EXPENSE
# ---------------------------------------------------

@login_required(login_url="/login/")
def add_expense(request):

    if request.method == "POST":

        form = ExpenseForm(request.POST)

        if form.is_valid():

            expense = form.save(commit=False)

            expense.user = request.user

            expense.save()

            return redirect("home")


    else:

        form = ExpenseForm()



    return render(
        request,
        "tracker/add_expense.html",
        {"form": form}
    )



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

        form = ExpenseForm(
            request.POST,
            instance=expense_obj
        )


        if form.is_valid():

            form.save()

            return redirect("home")


    else:

        form = ExpenseForm(
            instance=expense_obj
        )


    return render(
        request,
        "tracker/edit_expense.html",
        {"form": form}
    )



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


    return render(
        request,
        "tracker/delete_confirm.html",
        {"expense": expense_obj}
    )



# ---------------------------------------------------
# 🧾 SIGNUP PAGE
# ---------------------------------------------------

def signup(request):

    if request.method == "POST":

        form = SignUpForm(request.POST)


        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect("home")


    else:

        form = SignUpForm()



    return render(
        request,
        "tracker/signup.html",
        {"form": form}
    )



# ---------------------------------------------------
# 🔐 LOGIN VIEW
# ---------------------------------------------------

class CustomLoginView(LoginView):

    template_name = "tracker/login.html"

    redirect_authenticated_user = True



# ---------------------------------------------------
# 🚪 LOGOUT
# ---------------------------------------------------
def logout_view(request):

    logout(request)

    return redirect("signup")


# ---------------------------------------------------
# ROOT REDIRECT
# ---------------------------------------------------

def root_redirect(request):

    if request.user.is_authenticated:

        return redirect("home")


    return redirect("signup")

