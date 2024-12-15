from django.urls import path

from .views import LessonList, LessonDetail

urlpatterns = [
    path('', LessonList.as_view(), name='lesson-list'),
    path('<int:pk>/', LessonDetail.as_view(), name='lesson-detail'),
]
