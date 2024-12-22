from django.urls import path

from .views import PermissionGroupList, PermissionGroupDetail

urlpatterns = [
    path('', PermissionGroupList.as_view(), name='permission-group-list'),
    path('<int:pk>/', PermissionGroupDetail.as_view(), name='permission-group-detail')
]
