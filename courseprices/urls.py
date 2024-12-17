from django.urls import path

from .views import CoursePriceList, CoursePriceDetail

urlpatterns = [
    path('', CoursePriceList.as_view(), name='course-prices-list'),
    path('<int:pk>/', CoursePriceDetail.as_view(), name='course-price-detail')
]
