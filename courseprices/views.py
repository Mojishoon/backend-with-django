from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import CoursePrice

from courses.models import Course

from .serializers import CoursePriceSerializer, CoursePriceUpdateSerializer

from institutemanager.dependencies import pagination

from django.db.models import Q

from django.db import IntegrityError

class CoursePriceList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        size = request.query_params.get('size', 20)
        page = request.query_params.get('page', 1)
        course = request.query_params.get('course')
        from_price = request.query_params.get('from_price')
        to_price = request.query_params.get('to_price')
        from_date = request.query_params.get('from_date')
        to_date = request.query_params.get('to_date')
        if from_price or to_price or from_date or to_date or course:
            criteria = ((Q(course=course) if course else Q()) &
                        (Q(date__gte=from_date) if from_date else Q()) &
                        (Q(date__lte=to_date) if to_date else Q()) &
                        (Q(public_price__gte=from_price) if from_price else Q()) &
                        (Q(private_price__gte=from_price) if from_price else Q()) &
                        (Q(public_price__lte=to_price) if to_price else Q()) |
                        (Q(private_price__lte=to_price) if to_price else Q()))
        else:
            criteria = Q()
        paginated_course_price = pagination(CoursePrice, size, page, criteria)
        serializer = CoursePriceSerializer(paginated_course_price, many=True)
        return Response(serializer.data + [{"size": size, "page": page}])

    def post(self, request):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            request.data["recorder_id"] = request.user.id
            serializer = CoursePriceSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)



class CoursePriceDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            course_price = CoursePrice.objects.get(pk=pk)
            serializer = CoursePriceSerializer(course_price)
            return Response(serializer.data)
        except CoursePrice.DoesNotExist:
            return Response({"error": "course price not found"} ,status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            request.data["recorder_id"] = request.user.id
            course_price = CoursePrice.objects.get(pk=pk)
            course_price_data = CoursePriceUpdateSerializer(course_price).data
            course_price_data.update(request.data)
            serializer = CoursePriceUpdateSerializer(course_price, data=course_price_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CoursePrice.DoesNotExist:
            return Response({"error": "course price not found"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            course_price = Course.objects.get(pk=pk)
            course_price.delete()
            return Response({"massage": "course price deleted"}, status=status.HTTP_204_NO_CONTENT)
        except CoursePrice.DoesNotExist:
            return Response({"error": "course price not found"}, status=status.HTTP_404_NOT_FOUND)
