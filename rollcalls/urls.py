from django.urls import path

from .views import RollCallList, RollCallDetail

urlpatterns = [
    path('', RollCallList.as_view(), name='roll-call-list'),
    path('<int:pk>/', RollCallDetail.as_view(), name='roll-call-detail'),
]
