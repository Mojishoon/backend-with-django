from datetime import datetime

from inspect import currentframe

from django.db import IntegrityError
from drf_spectacular.utils import extend_schema, OpenApiParameter

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.views import TokenViewBase

from .models import User, LoginLog

from django.db.models import Q

from .serializers import UserSerializer, UserLoginSerializer, LoginLogSerializer

from institutemanager.dependencies import pagination, authorization

from django.contrib.auth.hashers import make_password


class UserList(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(parameters=[OpenApiParameter('page'),OpenApiParameter('size'),OpenApiParameter('search')])
    def get(self, request):
        operation = (self.__class__.__name__ + currentframe().f_code.co_name).lower()
        if authorization(request.user, operation):
            size = request.query_params.get('size', 20)
            page = request.query_params.get('page', 1)
            search = request.query_params.get('search')
            criteria = (Q(is_active = True) &
                        (Q(first_name__contains=search) |
                        Q(last_name__contains=search) |
                        Q(father_name__contains=search) |
                        Q(national_code__contains=search) |
                        Q(phone_number__contains=search))) if search else Q(is_active = True)
            paginated_users = pagination(User, size, page, criteria)
            serializer = UserSerializer(paginated_users, many=True)
            return Response(serializer.data + [{"size": size, "page": page}])

    @extend_schema(request=UserSerializer)
    def post(self, request):
        operation = (self.__class__.__name__ + currentframe().f_code.co_name).lower()
        if authorization(request.user, operation):
            try:
                request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
                request.data["recorder_id"] = request.user.id
                request.data["password"] = make_password(request.data["password"])
                existed_user = User.objects.filter(phone_number = request.data['phone_number'], is_active = False).first()
                if existed_user:
                    serializer = UserSerializer(existed_user, data = request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status = status.HTTP_201_CREATED)
                serializer = UserSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except IntegrityError as e:
                return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=UserSerializer)
    def put(self, request):
        operation = (self.__class__.__name__ + currentframe().f_code.co_name).lower()
        if authorization(request.user, operation):
            try:
                request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
                request.data["recorder_id"] = request.user.id
                user = User.objects.get(phone_number = request.data['phone_number'])
                if "password" in request.data:
                    request.data["password"] = make_password(request.data["password"])
                else:
                    request.data["password"] = user.password
                user_data = UserSerializer(user).data
                user_data.update(request.data)
                serializer = UserSerializer(user, data=user_data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            except IntegrityError as e:
                return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)




class UserDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        operation = (self.__class__.__name__ + currentframe().f_code.co_name).lower()
        if authorization(request.user, operation):
            try:
                user = User.objects.get(pk=pk, is_active=True)
                serializer = UserSerializer(user)
                return Response(serializer.data)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        operation = (self.__class__.__name__ + currentframe().f_code.co_name).lower()
        if authorization(request.user, operation):
            try:
                user = User.objects.get(pk=pk, is_active=True)
                if user:
                    user.is_active = False
                    user.save()
                    return Response({"message": "User deleted"}, status=status.HTTP_202_ACCEPTED)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            except IntegrityError as e:
                return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(TokenViewBase):

    @extend_schema(
        request=UserLoginSerializer
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = AccessToken.for_user(user)
        refresh = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(refresh), "access": str(token)}
        LoginLog.objects.create(user = user, login_date = datetime.now())
        User.objects.filter(pk=user.pk).update(last_login = datetime.now())
        return Response(data, status=status.HTTP_200_OK)


class LoginLogList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        operation = (self.__class__.__name__ + currentframe().f_code.co_name).lower()
        if authorization(request.user, operation):
            size = request.query_params.get('size', 20)
            page = request.query_params.get('page', 1)
            user = request.query_params.get('user')
            criteria = Q(user=user) if user else Q()
            paginated_login_log = pagination(LoginLog, size, page, criteria)
            serializer = LoginLogSerializer(paginated_login_log, many=True)
            return Response(serializer.data + [{"size": size, "page": page}])