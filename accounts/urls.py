from django.urls import path, include
from rest_framework.routers import SimpleRouter
from accounts import views


router = SimpleRouter()
router.register('accounts', views.AccountViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('accounts', views.ListAccount.as_view(), name='ListAccount'),
    # path('accounts/<str:pk>/', views.AccountDetails.as_view(), name='AccountDetails'),
    path("accounts/deposit", views.deposit),
    path("accounts/withdraw", views.withdraw),
]
