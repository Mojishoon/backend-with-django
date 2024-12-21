from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Holiday

from .serializers import HolidaySerializer

from institutemanager.dependencies import pagination

from django.db.models import Q

from django.db import IntegrityError

class HolidayList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        size = request.query_params.get('size', 20)
        page = request.query_params.get('page', 1)
        from_date = request.query_params.get('from_date')
        to_date = request.query_params.get('to_date')
        criteria = ((Q(date__gte=from_date) if from_date else Q()) &
                    (Q(date__lte=to_date) if to_date else Q()))
        paginated_holiday = pagination(Holiday, size, page, criteria)
        serializer = HolidaySerializer(paginated_holiday, many=True)
        return Response(serializer.data + [{"size": size, "page": page}])

    def post(self, request):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            request.data["recorder_id"] = request.user.id
            serializer = HolidaySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)



class HolidayDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            holiday = Holiday.objects.get(pk=pk)
            serializer = HolidaySerializer(holiday)
            return Response(serializer.data)
        except Holiday.DoesNotExist:
            return Response({"error": "holiday not found"} ,status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            request.data["recorder_id"] = request.user.id
            holiday = Holiday.objects.get(pk=pk)
            serializer = HolidaySerializer(holiday, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Holiday.DoesNotExist:
            return Response({"error": "holiday not found"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            holiday = Holiday.objects.get(pk=pk)
            holiday.delete()
            return Response({"massage": "holiday deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Holiday.DoesNotExist:
            return Response({"error": "holiday not found"}, status=status.HTTP_404_NOT_FOUND)
