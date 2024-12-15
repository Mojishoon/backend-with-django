from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import LessonGroup

from users.models import User

from .serializers import LessonGroupSerializer

from institutemanager.dependencies import pagination

from django.db.models import Q

from django.db import IntegrityError

class LessonGroupList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        size = request.query_params.get('size', 20)
        page = request.query_params.get('page', 1)
        q = request.query_params.get('q')
        if q:
            criteria = Q(name__contains=q)
        else:
            criteria = Q()
        paginated_lesson_group = pagination(LessonGroup, size, page, criteria)
        serializer = LessonGroupSerializer(paginated_lesson_group, many=True)
        return Response(serializer.data + [{"size": size, "page": page}])

    def post(self, request):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            serializer = LessonGroupSerializer(data=request.data)
            if serializer.is_valid():
                serializer.validated_data["recorder"] = User.objects.get(pk=request.user.id)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)



class LessonGroupDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            lesson_group = LessonGroup.objects.get(pk=pk)
            serializer = LessonGroupSerializer(lesson_group)
            return Response(serializer.data)
        except LessonGroup.DoesNotExist:
            return Response({"error": "lesson group not found"} ,status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            lesson_group = LessonGroup.objects.get(pk=pk)
            serializer = LessonGroupSerializer(lesson_group, data=request.data)
            if serializer.is_valid():
                serializer.validated_data["recorder"] = User.objects.get(pk=request.user.id)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except LessonGroup.DoesNotExist:
            return Response({"error": "lesson group not found"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            lesson_group = LessonGroup.objects.get(pk=pk)
            lesson_group.delete()
            return Response({"massage": "lesson_group deleted"}, status=status.HTTP_204_NO_CONTENT)
        except LessonGroup.DoesNotExist:
            return Response({"error": "lesson_group not found"}, status=status.HTTP_404_NOT_FOUND)
