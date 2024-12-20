from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import PayCategory

from .serializers import PayCategorySerializer

from institutemanager.dependencies import pagination

from django.db.models import Q

from django.db import IntegrityError

class PayCategoryList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        size = request.query_params.get('size', 20)
        page = request.query_params.get('page', 1)
        q = request.query_params.get('q')
        if q:
            criteria = Q(name__contains=q)
        else:
            criteria = Q()
        paginated_pay_category = pagination(PayCategory, size, page, criteria)
        serializer = PayCategorySerializer(paginated_pay_category, many=True)
        return Response(serializer.data + [{"size": size, "page": page}])

    def post(self, request):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            request.data["recorder_id"] = request.user.id
            serializer = PayCategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)



class PayCategoryDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            pay_category = PayCategory.objects.get(pk=pk)
            serializer = PayCategorySerializer(pay_category)
            return Response(serializer.data)
        except PayCategory.DoesNotExist:
            return Response({"error": "pay category not found"} ,status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            request.data["recorder_id"] = request.user.id
            pay_category = PayCategory.objects.get(pk=pk)
            serializer = PayCategorySerializer(pay_category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PayCategory.DoesNotExist:
            return Response({"error": "pay category not found"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            pay_category = PayCategory.objects.get(pk=pk)
            pay_category.delete()
            return Response({"massage": "pay category deleted"}, status=status.HTTP_204_NO_CONTENT)
        except PayCategory.DoesNotExist:
            return Response({"error": "pay category not found"}, status=status.HTTP_404_NOT_FOUND)
