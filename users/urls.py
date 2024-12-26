from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserList, UserDetail, UserLogin, LoginLogList


urlpatterns = [
    path('token/', UserLogin.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', UserList.as_view()),
    path('<int:pk>/', UserDetail.as_view()),
    path('login-logs/', LoginLogList.as_view())
]


