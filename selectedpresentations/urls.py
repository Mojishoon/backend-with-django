from django.urls import path

from .views import SelectedPresentationList, SelectedPresentationDetail

urlpatterns = [
    path('', SelectedPresentationList.as_view(), name='selected-presentation-list'),
    path('<int:pk>/', SelectedPresentationDetail.as_view(), name='selected-presentation-detail')
]
