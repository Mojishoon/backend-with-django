from django.urls import path

from .views import PermissionGroupDefineList, PermissionGroupDefineDetail

urlpatterns = [
    path('', PermissionGroupDefineList.as_view(), name='permission-group-define-list'),
    path('<int:pk>/', PermissionGroupDefineDetail.as_view(), name='permission-group-define-detail')
]
