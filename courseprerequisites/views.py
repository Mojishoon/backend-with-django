from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import CoursePrerequisite

from .serializers import CoursePrerequisiteSerializer, CoursePrerequisiteUpdateSerializer

from institutemanager.dependencies import pagination

from django.db.models import Q

from django.db import IntegrityError

class CoursePrerequisiteList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        size = request.query_params.get('size', 20)
        page = request.query_params.get('page', 1)
        course = request.query_params.get('course')
        prerequisite = request.query_params.get('prerequisite')
        criteria = ((Q(course=course) if course else Q()) &
                    (Q(prerequisite=prerequisite) if prerequisite else Q()))
        paginated_course_prerequisite = pagination(CoursePrerequisite, size, page, criteria)
        serializer = CoursePrerequisiteSerializer(paginated_course_prerequisite, many=True)
        return Response(serializer.data + [{"size": size, "page": page}])

    def post(self, request):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            request.data["recorder_id"] = request.user.id
            serializer = CoursePrerequisiteSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            course = request.query_params.get('course')
            prerequisite = request.query_params.get('prerequisite')
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            request.data["recorder_id"] = request.user.id
            course_prerequisite = CoursePrerequisite.objects.get(course=course, prerequisite=prerequisite)
            course_prerequisite_data = CoursePrerequisiteUpdateSerializer(course_prerequisite).data
            course_prerequisite_data.update(request.data)
            serializer = CoursePrerequisiteUpdateSerializer(course_prerequisite, data=course_prerequisite_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CoursePrerequisite.DoesNotExist:
            return Response({"error": "course prerequisite not found"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            course = request.query_params.get('course')
            prerequisite = request.query_params.get('prerequisite')
            course_prerequisite = CoursePrerequisite.objects.get(course=course, prerequisite=prerequisite)
            course_prerequisite.delete()
            return Response({"massage": "course prerequisite deleted"}, status=status.HTTP_204_NO_CONTENT)
        except CoursePrerequisite.DoesNotExist:
            return Response({"error": "course prerequisite not found"}, status=status.HTTP_404_NOT_FOUND)
