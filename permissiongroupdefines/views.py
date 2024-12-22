from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import PermissionGroupDefine

from .serializers import PermissionGroupDefineSerializer, PermissionGroupDefineUpdateSerializer

from institutemanager.dependencies import pagination

from django.db.models import Q

from django.db import IntegrityError

class PermissionGroupDefineList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        size = request.query_params.get('size', 20)
        page = request.query_params.get('page', 1)
        permission = request.query_params.get('permission')
        permission_group = request.query_params.get('permission_group')
        criteria = ((Q(permission=permission) if permission else Q()) &
                    (Q(permission_group=permission_group) if permission_group else Q()))
        paginated_permission_group_define = pagination(PermissionGroupDefine, size, page, criteria)
        serializer = PermissionGroupDefineSerializer(paginated_permission_group_define, many=True)
        return Response(serializer.data + [{"size": size, "page": page}])

    def post(self, request):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            request.data["recorder_id"] = request.user.id
            serializer = PermissionGroupDefineSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)


class PermissionGroupDefineDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            permission_group_define = PermissionGroupDefine.objects.get(pk=pk)
            serializer = PermissionGroupDefineSerializer(permission_group_define)
            return Response(serializer.data)
        except PermissionGroupDefine.DoesNotExist:
            return Response({"error": "permission group define not found"} ,status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            request.data["recorder_id"] = request.user.id
            permission_group_define = PermissionGroupDefine.objects.get(pk=pk)
            permission_group_define_data = PermissionGroupDefineUpdateSerializer(permission_group_define).data
            permission_group_define_data.update(request.data)
            serializer = PermissionGroupDefineUpdateSerializer(
                permission_group_define, data=permission_group_define_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PermissionGroupDefine.DoesNotExist:
            return Response({"error": "permission group define not found"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            permission_group_define = PermissionGroupDefine.objects.get(pk=pk)
            permission_group_define.delete()
            return Response({"massage": "permission group define deleted"}, status=status.HTTP_204_NO_CONTENT)
        except PermissionGroupDefine.DoesNotExist:
            return Response({"error": "permission group define not found"}, status=status.HTTP_404_NOT_FOUND)
