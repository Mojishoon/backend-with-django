from django.urls import path

from .views import CoursePrerequisiteList

urlpatterns = [
    path('', CoursePrerequisiteList.as_view(), name='course-prerequisite-list')
]
