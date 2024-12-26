from datetime import datetime

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Role

from .serializers import RoleSerializer, RoleRequestSerializer

from institutemanager.dependencies import pagination, authorization

from django.db.models import Q

from django.db import IntegrityError

from inspect import currentframe


class RoleList(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(parameters=[OpenApiParameter('page'), OpenApiParameter('size'), OpenApiParameter('search')])
    def get(self, request):
        operation = (self.__class__.__name__ + currentframe().f_code.co_name).lower()
        if authorization(request.user, operation):
            size = request.query_params.get('size', 20)
            page = request.query_params.get('page', 1)
            search = request.query_params.get('search')
            criteria = Q(name__contains=search) if search else Q()
            paginated_roles = pagination(Role, size, page, criteria)
            serializer = RoleSerializer(paginated_roles, many=True)
            return Response(serializer.data + [{"size": size, "page": page}])


    @extend_schema(request=RoleRequestSerializer)
    def post(self, request):
        operation = (self.__class__.__name__ + currentframe().f_code.co_name).lower()
        if authorization(request.user, operation):
            try:
                request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
                request.data["recorder_id"] = request.user.id
                serializer = RoleSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except IntegrityError as e:
                return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)



class RoleDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        operation = (self.__class__.__name__ + currentframe().f_code.co_name).lower()
        if authorization(request.user, operation):
            try:
                role = Role.objects.get(pk=pk)
                serializer = RoleSerializer(role)
                return Response(serializer.data)
            except Role.DoesNotExist:
                return Response({"error": "role not found"} ,status=status.HTTP_404_NOT_FOUND)


    @extend_schema(request=RoleRequestSerializer)
    def put(self, request, pk):
        operation = (self.__class__.__name__ + currentframe().f_code.co_name).lower()
        if authorization(request.user, operation):
            try:
                request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
                request.data["recorder_id"] = request.user.id
                role = Role.objects.get(pk=pk)
                role_data = RoleSerializer(role).data
                role_data.update(request.data)
                serializer = RoleSerializer(role, data=role_data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Role.DoesNotExist:
                return Response({"error": "role not found"}, status=status.HTTP_404_NOT_FOUND)
            except IntegrityError as e:
                return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        operation = (self.__class__.__name__ + currentframe().f_code.co_name).lower()
        if authorization(request.user, operation):
            try:
                role = Role.objects.get(pk=pk)
                role.delete()
                return Response({"massage": "role deleted"}, status=status.HTTP_202_ACCEPTED)
            except Role.DoesNotExist:
                return Response({"error": "role not found"}, status=status.HTTP_404_NOT_FOUND)
            except IntegrityError as e:
                return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)

