from django.urls import path

from .views import FinancialTransactionList, FinancialTransactionDetail

urlpatterns = [
    path('', FinancialTransactionList.as_view(), name='financial-transaction-list'),
    path('<int:pk>/', FinancialTransactionDetail.as_view(), name='financial-transaction-detail')
]
