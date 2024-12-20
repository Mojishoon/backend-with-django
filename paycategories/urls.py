from django.urls import path

from .views import PayCategoryList, PayCategoryDetail

urlpatterns = [
    path('', PayCategoryList.as_view(), name='pay-category-list'),
    path('<int:pk>/', PayCategoryDetail.as_view(), name='pay-category-detail')
]
