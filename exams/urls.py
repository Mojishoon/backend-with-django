from django.urls import path

from .views import ExamList, ExamDetail

urlpatterns = [
    path('', ExamList.as_view(), name='exam-list'),
    path('<int:pk>/', ExamDetail.as_view(), name='exam-detail')
]
