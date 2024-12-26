from datetime import datetime

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import FinancialTransaction

from .serializers import (FinancialTransactionSerializer, FinancialTransactionUpdateSerializer,
                          FinancialTransactionRequestSerializer)

from institutemanager.dependencies import pagination

from django.db.models import Q

from django.db import IntegrityError

class FinancialTransactionList(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(parameters=[OpenApiParameter('page'), OpenApiParameter('size'), OpenApiParameter('user'),
                               OpenApiParameter('financial_category'), OpenApiParameter('pay_category'),
                               OpenApiParameter('from_date', datetime), OpenApiParameter('to_date', datetime)])
    def get(self, request):
        size = request.query_params.get('size', 20)
        page = request.query_params.get('page', 1)
        user = request.query_params.get('user')
        financial_category = request.query_params.get('financial_category')
        pay_category = request.query_params.get('pay_category')
        from_date = request.query_params.get('from_date')
        to_date = request.query_params.get('to_date')
        criteria = ((Q(user=user) if user else Q()) &
                    (Q(financial_category=financial_category) if financial_category else Q()) &
                    (Q(transaction_date__gte=from_date) if from_date else Q()) &
                    (Q(transaction__lte=to_date) if to_date else Q()) &
                    (Q(pay_category=pay_category) if pay_category else Q()))
        paginated_financial_transaction = pagination(FinancialTransaction, size, page, criteria)
        serializer = FinancialTransactionSerializer(paginated_financial_transaction, many=True)
        return Response(serializer.data + [{"size": size, "page": page}])


    @extend_schema(request=FinancialTransactionRequestSerializer)
    def post(self, request):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            request.data["recorder_id"] = request.user.id
            x = 0
            if "presentation_id" in request.data and request.data["presentation_id"]:
                x += 1
            if "selected_presentation_id" in request.data and request.data["selected_presentation_id"]:
                x += 1
            if "selected_exam_id" in request.data and request.data["selected_exam_id"]:
                x += 1
            if x > 1:
                return Response(
                    {"error": "one of presentation_id , selected_presentation_id and selected_exam_id must enter"},
                    status=status.HTTP_400_BAD_REQUEST)

            serializer = FinancialTransactionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)


class FinancialTransactionDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            financial_transaction = FinancialTransaction.objects.get(pk=pk)
            serializer = FinancialTransactionSerializer(financial_transaction)
            return Response(serializer.data)
        except FinancialTransaction.DoesNotExist:
            return Response({"error": "financial transaction not found"} ,status=status.HTTP_404_NOT_FOUND)


    @extend_schema(request=FinancialTransactionRequestSerializer)
    def put(self, request, pk):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            request.data["recorder_id"] = request.user.id
            financial_transaction = FinancialTransaction.objects.get(pk=pk)
            financial_transaction_data = FinancialTransactionUpdateSerializer(financial_transaction).data
            financial_transaction_data.update(request.data)
            x = 0

            if "presentation_id" in request.data and request.data["presentation_id"]:
                x += 1
            if "selected_presentation_id" in request.data and request.data["selected_presentation_id"]:
                x += 1
            if "selected_exam_id" in request.data and request.data["selected_exam_id"]:
                x += 1

            if (
                    not financial_transaction_data["presentation"] and
                "presentation_id" in request.data and
                request.data["presentation_id"]
            ):
                x += 1
            if (
                not financial_transaction_data["selected_presentation"] and
                "selected_presentation_id" in request.data and
                request.data["selected_presentation_id"]
            ):
                x += 1
            if (
                not financial_transaction_data["selected_exam"] and
                "selected_exam_id" in request.data and
                request.data["selected_exam_id"]
            ):
                x += 1

            if x > 1:
                return Response(
                    {"error": "one of presentation_id , selected_presentation_id and selected_exam_id must enter"},
                    status=status.HTTP_400_BAD_REQUEST)

            serializer = FinancialTransactionUpdateSerializer(financial_transaction, data=financial_transaction_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except FinancialTransaction.DoesNotExist:
            return Response({"error": "financial transaction not found"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            financial_transaction = FinancialTransaction.objects.get(pk=pk)
            financial_transaction.delete()
            return Response({"massage": "financial transaction deleted"}, status=status.HTTP_202_ACCEPTED)
        except FinancialTransaction.DoesNotExist:
            return Response({"error": "financial transaction not found"}, status=status.HTTP_404_NOT_FOUND)
