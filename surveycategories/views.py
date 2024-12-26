from datetime import datetime

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import SurveyCategory

from .serializers import SurveyCategorySerializer, SurveyCategoryRequestSerializer

from institutemanager.dependencies import pagination

from django.db.models import Q

from django.db import IntegrityError

class SurveyCategoryList(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(parameters=[OpenApiParameter('page'), OpenApiParameter('size'), OpenApiParameter('search')])
    def get(self, request):
        size = request.query_params.get('size', 20)
        page = request.query_params.get('page', 1)
        search = request.query_params.get('search')
        criteria = Q(name__contains=search) if search else Q()
        paginated_survey_category = pagination(SurveyCategory, size, page, criteria)
        serializer = SurveyCategorySerializer(paginated_survey_category, many=True)
        return Response(serializer.data + [{"size": size, "page": page}])


    @extend_schema(request=SurveyCategoryRequestSerializer)
    def post(self, request):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            request.data["recorder_id"] = request.user.id
            serializer = SurveyCategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)



class SurveyCategoryDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            survey_category = SurveyCategory.objects.get(pk=pk)
            serializer = SurveyCategorySerializer(survey_category)
            return Response(serializer.data)
        except SurveyCategory.DoesNotExist:
            return Response({"error": "survey category not found"} ,status=status.HTTP_404_NOT_FOUND)


    @extend_schema(request=SurveyCategoryRequestSerializer)
    def put(self, request, pk):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            request.data["recorder_id"] = request.user.id
            survey_category = SurveyCategory.objects.get(pk=pk)
            serializer = SurveyCategorySerializer(survey_category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except SurveyCategory.DoesNotExist:
            return Response({"error": "survey category not found"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            survey_category = SurveyCategory.objects.get(pk=pk)
            survey_category.delete()
            return Response({"massage": "survey category deleted"}, status=status.HTTP_202_ACCEPTED)
        except SurveyCategory.DoesNotExist:
            return Response({"error": "survey category not found"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)
