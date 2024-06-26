from django.urls import path

from accounts import views

urlpatterns = [
    path('accounts', views.list_accounts),
    path('accounts/<str:pk>/', views.accounts_details),
    path("accounts/deposit", views.deposit),
    path("accounts/withdraw", views.withdraw),
]
