from datetime import datetime

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import PermissionGroup

from .serializers import PermissionGroupSerializer, PermissionGroupRequestSerializer

from institutemanager.dependencies import pagination

from django.db.models import Q

from django.db import IntegrityError

class PermissionGroupList(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(parameters=[OpenApiParameter('size'), OpenApiParameter('page'), OpenApiParameter('search')])
    def get(self, request):
        size = request.query_params.get('size', 20)
        page = request.query_params.get('page', 1)
        search = request.query_params.get('search')
        criteria = Q(name__contains=search) if search else Q()
        paginated_permission_group = pagination(PermissionGroup, size, page, criteria)
        serializer = PermissionGroupSerializer(paginated_permission_group, many=True)
        return Response(serializer.data + [{"size": size, "page": page}])


    @extend_schema(request=PermissionGroupRequestSerializer)
    def post(self, request):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            request.data["recorder_id"] = request.user.id
            serializer = PermissionGroupSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)



class PermissionGroupDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            permission_group = PermissionGroup.objects.get(pk=pk)
            serializer = PermissionGroupSerializer(permission_group)
            return Response(serializer.data)
        except PermissionGroup.DoesNotExist:
            return Response({"error": "permission group not found"} ,status=status.HTTP_404_NOT_FOUND)


    @extend_schema(request=PermissionGroupRequestSerializer)
    def put(self, request, pk):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            request.data["recorder_id"] = request.user.id
            permission_group = PermissionGroup.objects.get(pk=pk)
            serializer = PermissionGroupSerializer(permission_group, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PermissionGroup.DoesNotExist:
            return Response({"error": "permission group not found"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            permission_group = PermissionGroup.objects.get(pk=pk)
            permission_group.delete()
            return Response({"massage": "permission group deleted"}, status=status.HTTP_202_ACCEPTED)
        except PermissionGroup.DoesNotExist:
            return Response({"error": "permission group not found"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)
