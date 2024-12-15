from datetime import datetime

from django.db import IntegrityError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from roles.models import Role

from .models import User

from django.db.models import Q

from .serializers import UserSerializer

from institutemanager.dependencies import pagination

from django.contrib.auth.hashers import make_password


class UserList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        size = request.query_params.get('size', 20)
        page = request.query_params.get('page', 1)
        q = request.query_params.get('q')
        if q:
            criteria = (Q(is_active = True) &
                        (Q(first_name__contains=q) |
                        Q(last_name__contains=q) |
                        Q(father_name__contains=q) |
                        Q(national_code__contains=q) |
                        Q(phone_number__contains=q)))
        else:
            criteria = Q(is_active = True)
        paginated_users = pagination(User, size, page, criteria)
        serializer = UserSerializer(paginated_users, many=True)
        return Response(serializer.data + [{"size": size, "page": page}])

    def post(self, request):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            existed_user = User.objects.filter(phone_number = request.data['phone_number'], is_active = False).first()
            if existed_user:
                serializer = UserSerializer(existed_user, data = request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status = status.HTTP_201_CREATED)
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                if "role" in request.data:
                    serializer.validated_data["role"] = Role.objects.get(id=request.data["role"])
                serializer.validated_data["recorder"] = User.objects.get(id=request.user.id)
                serializer.validated_data["password"] = make_password(request.data["password"])
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            user = User.objects.get(phone_number = request.data['phone_number'])
            if "password" in request.data:
                request.data["password"] = make_password(request.data["password"])
            else:
                request.data["password"] = user.password
            user_data = UserSerializer(user).data
            user_data.update(request.data)
            serializer = UserSerializer(user, data=user_data)
            if serializer.is_valid():
                if "role" in request.data:
                    serializer.validated_data["role"] = Role.objects.get(id=user_data["role"])
                else:
                    serializer.validated_data["role"] = Role.objects.get(id=user_data["role"]["id"])
                serializer.validated_data["recorder"] = User.objects.get(id=request.user.id)
                serializer.save()
                return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)




class UserDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk, is_active=True)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk, is_active=True)
            if user:
                user.is_active = False
                user.save()
                return Response({"message": "User deleted"}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
