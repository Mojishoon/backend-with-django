from django.urls import path

from .views import LessonGroupList, LessonGroupDetail

urlpatterns = [
    path('', LessonGroupList.as_view(), name='lesson-group-list'),
    path('<int:pk>/', LessonGroupDetail.as_view(), name='lesson-group-detail'),
]
