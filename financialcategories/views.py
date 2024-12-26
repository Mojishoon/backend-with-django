from datetime import datetime

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import FinancialCategory

from .serializers import FinancialCategorySerializer, FinancialCategoryRequestSerializer

from institutemanager.dependencies import pagination, authorization

from django.db.models import Q

from django.db import IntegrityError

from inspect import currentframe

class FinancialCategoryList(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(parameters=[OpenApiParameter('page'), OpenApiParameter('size'), OpenApiParameter('search')])
    def get(self, request):
        operation = (self.__class__.__name__ + currentframe().f_code.co_name).lower()
        if authorization(request.user, operation):
            size = request.query_params.get('size', 20)
            page = request.query_params.get('page', 1)
            search = request.query_params.get('search')
            criteria = Q(name__contains=search) if search else Q()
            paginated_financial_category = pagination(FinancialCategory, size, page, criteria)
            serializer = FinancialCategorySerializer(paginated_financial_category, many=True)
            return Response(serializer.data + [{"size": size, "page": page}])


    @extend_schema(request=FinancialCategoryRequestSerializer)
    def post(self, request):
        operation = (self.__class__.__name__ + currentframe().f_code.co_name).lower()
        if authorization(request.user, operation):
            try:
                request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
                request.data["recorder_id"] = request.user.id
                serializer = FinancialCategorySerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except IntegrityError as e:
                return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)



class FinancialCategoryDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        operation = (self.__class__.__name__ + currentframe().f_code.co_name).lower()
        if authorization(request.user, operation):
            try:
                financial_category = FinancialCategory.objects.get(pk=pk)
                serializer = FinancialCategorySerializer(financial_category)
                return Response(serializer.data)
            except FinancialCategory.DoesNotExist:
                return Response({"error": "financial category not found"} ,status=status.HTTP_404_NOT_FOUND)


    @extend_schema(request=FinancialCategoryRequestSerializer)
    def put(self, request, pk):
        operation = (self.__class__.__name__ + currentframe().f_code.co_name).lower()
        if authorization(request.user, operation):
            try:
                request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
                request.data["recorder_id"] = request.user.id
                financial_category = FinancialCategory.objects.get(pk=pk)
                serializer = FinancialCategorySerializer(financial_category, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except FinancialCategory.DoesNotExist:
                return Response({"error": "financial category not found"}, status=status.HTTP_404_NOT_FOUND)
            except IntegrityError as e:
                return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        operation = (self.__class__.__name__ + currentframe().f_code.co_name).lower()
        if authorization(request.user, operation):
            try:
                financial_category = FinancialCategory.objects.get(pk=pk)
                financial_category.delete()
                return Response({"massage": "financial category deleted"}, status=status.HTTP_202_ACCEPTED)
            except FinancialCategory.DoesNotExist:
                return Response({"error": "financial category not found"}, status=status.HTTP_404_NOT_FOUND)
            except IntegrityError as e:
                return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)
