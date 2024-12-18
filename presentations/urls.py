from django.urls import path

from .views import PresentationList, PresentationDetail

urlpatterns = [
    path('', PresentationList.as_view(), name='presentation-list'),
    path('<int:pk>/', PresentationDetail.as_view(), name='presentation-detail'),
]
