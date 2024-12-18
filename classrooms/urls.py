from django.urls import path

from .views import ClassroomList, ClassroomDetail

urlpatterns = [
    path('', ClassroomList.as_view(), name='classrooms'),
    path('<int:pk>/', ClassroomDetail.as_view(), name='classroom')
]
