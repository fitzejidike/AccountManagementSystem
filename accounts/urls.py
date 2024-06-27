from django.urls import path

from accounts import views

urlpatterns = [
    path('accounts', views.ListAccount.as_view(), name='ListAccount'),
    path('accounts/<str:pk>/', views.AccountDetails.as_view(), name='AccountDetails'),
    path("accounts/deposit", views.deposit),
    path("accounts/withdraw", views.withdraw),
]
