from datetime import datetime

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import LessonGroup

from .serializers import LessonGroupSerializer, LessonGroupRequestSerializer

from institutemanager.dependencies import pagination

from django.db.models import Q

from django.db import IntegrityError

class LessonGroupList(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(parameters=[OpenApiParameter('page'), OpenApiParameter('size'), OpenApiParameter('search')])
    def get(self, request):
        size = request.query_params.get('size', 20)
        page = request.query_params.get('page', 1)
        search = request.query_params.get('search')
        criteria = Q(name__contains=search) if search else Q()
        paginated_lesson_group = pagination(LessonGroup, size, page, criteria)
        serializer = LessonGroupSerializer(paginated_lesson_group, many=True)
        return Response(serializer.data + [{"size": size, "page": page}])


    @extend_schema(request=LessonGroupRequestSerializer)
    def post(self, request):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            request.data["recorder_id"] = request.user.id
            serializer = LessonGroupSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)



class LessonGroupDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            lesson_group = LessonGroup.objects.get(pk=pk)
            serializer = LessonGroupSerializer(lesson_group)
            return Response(serializer.data)
        except LessonGroup.DoesNotExist:
            return Response({"error": "lesson group not found"} ,status=status.HTTP_404_NOT_FOUND)


    @extend_schema(request=LessonGroupRequestSerializer)
    def put(self, request, pk):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            request.data["recorder_id"] = request.user.id
            lesson_group = LessonGroup.objects.get(pk=pk)
            serializer = LessonGroupSerializer(lesson_group, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except LessonGroup.DoesNotExist:
            return Response({"error": "lesson group not found"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            lesson_group = LessonGroup.objects.get(pk=pk)
            lesson_group.delete()
            return Response({"massage": "lesson group deleted"}, status=status.HTTP_202_ACCEPTED)
        except LessonGroup.DoesNotExist:
            return Response({"error": "lesson group not found"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)
