from django.urls import path

from .views import HolidayList, HolidayDetail

urlpatterns = [
    path('', HolidayList.as_view(), name='holidays-list'),
    path('<int:pk>/', HolidayDetail.as_view(), name='holidays-detail')
]
