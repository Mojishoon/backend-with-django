from django.urls import path

from .views import PresentationSurveyList, PresentationSurveyDetail

urlpatterns = [
    path('', PresentationSurveyList.as_view(), name='presentation-surveys-list'),
    path('<int:pk>/', PresentationSurveyDetail.as_view(), name='presentation-surveys-detail')
]
