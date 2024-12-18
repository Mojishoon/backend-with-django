from django.urls import path

from .views import BuildingList, BuildingDetail

urlpatterns = [
    path('', BuildingList.as_view(), name='building-list'),
    path('<int:pk>/', BuildingDetail.as_view(), name='building-detail')
]
