from datetime import datetime

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import ExamSchedule

from .serializers import ExamScheduleSerializer, ExamScheduleUpdateSerializer, ExamScheduleRequestSerializer

from institutemanager.dependencies import pagination

from django.db.models import Q

from django.db import IntegrityError

class ExamScheduleList(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(parameters=[OpenApiParameter('size'), OpenApiParameter('page'), OpenApiParameter('exam'),
                               OpenApiParameter('from_date', datetime), OpenApiParameter('to_date', datetime)])
    def get(self, request):
        size = request.query_params.get('size', 20)
        page = request.query_params.get('page', 1)
        exam = request.query_params.get('exam')
        from_date = request.query_params.get('from_date')
        to_date = request.query_params.get('to_date')
        criteria = ((Q(exam=exam) if exam else Q()) &
                    (Q(start_date__gte=from_date) if from_date else Q()) &
                    (Q(start_date__lte=to_date) if to_date else Q()))
        paginated_exam_schedule = pagination(ExamSchedule, size, page, criteria)
        serializer = ExamScheduleSerializer(paginated_exam_schedule, many=True)
        return Response(serializer.data + [{"size": size, "page": page}])


    @extend_schema(request=ExamScheduleRequestSerializer)
    def post(self, request):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            request.data["recorder_id"] = request.user.id
            serializer = ExamScheduleSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)



class ExamScheduleDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            exam_schedule = ExamSchedule.objects.get(pk=pk)
            serializer = ExamScheduleSerializer(exam_schedule)
            return Response(serializer.data)
        except ExamSchedule.DoesNotExist:
            return Response({"error": "exam schedule not found"} ,status=status.HTTP_404_NOT_FOUND)


    @extend_schema(request=ExamScheduleRequestSerializer)
    def put(self, request, pk):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            request.data["recorder_id"] = request.user.id
            exam_schedule = ExamSchedule.objects.get(pk=pk)
            exam_schedule_data = ExamScheduleUpdateSerializer(exam_schedule).data
            exam_schedule_data.update(request.data)
            serializer = ExamScheduleUpdateSerializer(exam_schedule, data=exam_schedule_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ExamSchedule.DoesNotExist:
            return Response({"error": "exam schedule not found"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            exam_schedule = ExamSchedule.objects.get(pk=pk)
            exam_schedule.delete()
            return Response({"massage": "exam schedule deleted"}, status=status.HTTP_202_ACCEPTED)
        except ExamSchedule.DoesNotExist:
            return Response({"error": "exam schedule not found"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)
