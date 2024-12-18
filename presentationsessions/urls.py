from django.urls import path

from .views import PresentationSessionList, PresentationSessionDetail

urlpatterns = [
    path('', PresentationSessionList.as_view(), name='presentation-session-list'),
    path('<int:pk>/', PresentationSessionDetail.as_view(), name='presentation-session-detail')
]
