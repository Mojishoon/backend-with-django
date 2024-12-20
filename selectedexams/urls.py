from django.urls import path

from .views import SelectedExamList, SelectedExamDetail

urlpatterns = [
    path('', SelectedExamList.as_view(), name='selected-exam-list'),
    path('<int:pk>/', SelectedExamDetail.as_view(), name='selected-exam-detail')
]
