from django.urls import path

from .views import SurveyCategoryList, SurveyCategoryDetail

urlpatterns = [
    path('', SurveyCategoryList.as_view(), name='survey-category-list'),
    path('<int:pk>/', SurveyCategoryDetail.as_view(), name='survey-category-detail')
]
