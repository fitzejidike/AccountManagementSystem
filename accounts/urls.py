from django.urls import path

from account import views

urlpatterns = [
    path('accounts', views.list_accounts),
    path('accounts/<str:pk>/', views.accounts_details)
]
