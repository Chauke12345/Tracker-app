from django.urls import path
from . import views
from .views import CustomLoginView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.expense_list, name='home'),
    path('add/', views.add_expense, name='add_expense'),

    path('signup/', views.signup, name='signup'),

    path("login/", CustomLoginView.as_view(), name="login"),

    path('logout/', views.logout_view, name='logout'),
    path('edit/<int:id>/', views.edit_expense, name='edit_expense'),
    path('delete/<int:id>/', views.delete_expense, name='delete_expense'),

    path("expenses/", views.expense_list, name="expense_list"),
]