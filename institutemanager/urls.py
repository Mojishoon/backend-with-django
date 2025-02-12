"""
URL configuration for institutemanager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('permissions/', include('permissions.urls')),
    path('permission-groups/', include('permissiongroups.urls')),
    path('permission-group-defines/', include('permissiongroupdefines.urls')),
    path('roles/', include('roles.urls')),
    path('lesson-groups/', include('lessongroups.urls')),
    path('lessons/', include('lessons.urls')),
    path('courses/', include('courses.urls')),
    path('course-prices/', include('courseprices.urls')),
    path('course-prerequisites/', include('courseprerequisites.urls')),
    path('buildings/', include('buildings.urls')),
    path('classrooms/', include('classrooms.urls')),
    path('presentations/', include('presentations.urls')),
    path('selected-presentations/', include('selectedpresentations.urls')),
    path('presentation-sessions/', include('presentationsessions.urls')),
    path('roll-calls/', include('rollcalls.urls')),
    path('survey-categories/', include('surveycategories.urls')),
    path('presentation-surveys/', include('presentationsurveys.urls')),
    path('exams/', include('exams.urls')),
    path('exam-schedules/', include('examschedules.urls')),
    path('selected-exams/', include('selectedexams.urls')),
    path('financial-categories/', include('financialcategories.urls')),
    path('pay-categories/', include('paycategories.urls')),
    path('financial-transactions/', include('financialtransactions.urls')),
    path('holidays/', include('holidays.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc')
]
