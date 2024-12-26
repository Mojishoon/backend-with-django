from datetime import datetime

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Building

from .serializers import BuildingSerializer, BuildingRequestSerializer

from institutemanager.dependencies import pagination

from django.db.models import Q

from django.db import IntegrityError

class BuildingList(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(parameters=[OpenApiParameter('search'), OpenApiParameter('page'), OpenApiParameter('size')])
    def get(self, request):
        size = request.query_params.get('size', 20)
        page = request.query_params.get('page', 1)
        search = request.query_params.get('search')
        criteria = Q(name__contains=search) if search else Q()
        paginated_building = pagination(Building, size, page, criteria)
        serializer = BuildingSerializer(paginated_building, many=True)
        return Response(serializer.data + [{"size": size, "page": page}])


    @extend_schema(request=BuildingRequestSerializer)
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
            return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)



class BuildingDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            building = Building.objects.get(pk=pk)
            serializer = BuildingSerializer(building)
            return Response(serializer.data)
        except Building.DoesNotExist:
            return Response({"error": "building not found"} ,status=status.HTTP_404_NOT_FOUND)

    @extend_schema(request=BuildingRequestSerializer)
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
            return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        try:
            building = Building.objects.get(pk=pk)
            building.delete()
            return Response({"massage": "building deleted"}, status=status.HTTP_202_ACCEPTED)
        except Building.DoesNotExist:
            return Response({"error": "building not found"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)
