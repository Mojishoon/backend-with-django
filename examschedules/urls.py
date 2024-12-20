from django.urls import path

from .views import ExamScheduleList, ExamScheduleDetail

urlpatterns = [
    path('', ExamScheduleList.as_view(), name='exam-schedule-list'),
    path('<int:pk>/', ExamScheduleDetail.as_view(), name='exam-schedule-detail')
]
