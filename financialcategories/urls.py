from django.urls import path

from .views import FinancialCategoryList, FinancialCategoryDetail

urlpatterns = [
    path('', FinancialCategoryList.as_view(), name='financial-category-list'),
    path('<int:pk>/', FinancialCategoryDetail.as_view(), name='financial-category-detail')
]
