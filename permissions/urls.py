from django.urls import path

from .views import PermissionList, PermissionDetail

urlpatterns = [
    path('permissions/', PermissionList.as_view(), name='permission-list'),
    path('permissions/<int:pk>/', PermissionDetail.as_view(), name='permission-detail')
]
