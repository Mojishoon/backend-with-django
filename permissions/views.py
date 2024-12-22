from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Permission

from .serializers import PermissionSerializer

from institutemanager.dependencies import pagination

from django.db.models import Q

class PermissionList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        size = request.query_params.get('size', 20)
        page = request.query_params.get('page', 1)
        q = request.query_params.get('q')
        criteria = Q(name__contains=q) if q else Q()
        paginated_permission = pagination(Permission, size, page, criteria)
        serializer = PermissionSerializer(paginated_permission, many=True)
        return Response(serializer.data + [{"size": size, "page": page}])


class PermissionDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            permission = Permission.objects.get(pk=pk)
            serializer = PermissionSerializer(permission)
            return Response(serializer.data)
        except Permission.DoesNotExist:
            return Response({"error": "permission not found"} ,status=status.HTTP_404_NOT_FOUND)
