from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
from .views import CustomLoginView


urlpatterns = [

    # ROOT
    path('', views.root_redirect, name='root'),


    # AUTH
    path('signup/', views.signup, name='signup'),

    path(
        "login/",
        CustomLoginView.as_view(),
        name="login"
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),


    # APP
    path(
        'home/',
        views.expense_list,
        name='home'
    ),

    path(
        'add/',
        views.add_expense,
        name='add_expense'
    ),

    path(
        'edit/<int:id>/',
        views.edit_expense,
        name='edit_expense'
    ),

    path(
        'delete/<int:id>/',
        views.delete_expense,
        name='delete_expense'
    ),

]


# MEDIA FILES
if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )