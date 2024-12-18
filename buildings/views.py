from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Building

from .serializers import BuildingSerializer

from institutemanager.dependencies import pagination

from django.db.models import Q

from django.db import IntegrityError

class BuildingList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        size = request.query_params.get('size', 20)
        page = request.query_params.get('page', 1)
        q = request.query_params.get('q')
        if q:
            criteria = Q(name__contains=q)
        else:
            criteria = Q()
        paginated_lesson_group = pagination(Building, size, page, criteria)
        serializer = BuildingSerializer(paginated_lesson_group, many=True)
        return Response(serializer.data + [{"size": size, "page": page}])

    def post(self, request):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            request.data["recorder_id"] = request.user.id
            serializer = BuildingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)



class BuildingDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            building = Building.objects.get(pk=pk)
            serializer = BuildingSerializer(building)
            return Response(serializer.data)
        except Building.DoesNotExist:
            return Response({"error": "building not found"} ,status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            request.data["recorder_id"] = request.user.id
            building = Building.objects.get(pk=pk)
            serializer = BuildingSerializer(building, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Building.DoesNotExist:
            return Response({"error": "building not found"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            building = Building.objects.get(pk=pk)
            building.delete()
            return Response({"massage": "building deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Building.DoesNotExist:
            return Response({"error": "building not found"}, status=status.HTTP_404_NOT_FOUND)
