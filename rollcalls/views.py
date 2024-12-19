from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import RollCall

from .serializers import RollCallSerializer, RollCallUpdateSerializer

from institutemanager.dependencies import pagination

from django.db.models import Q

from django.db import IntegrityError

class RollCallList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        size = request.query_params.get('size', 20)
        page = request.query_params.get('page', 1)
        presentation_session = request.query_params.get('presentation_session')
        student = request.query_params.get('student')
        is_present = request.query_params.get('is_present')
        if student or presentation_session or is_present:
            criteria = ((Q(student=student) if student else Q()) &
                        (Q(presentation_session=presentation_session) if presentation_session else Q()) &
                        (Q(is_present=is_present) if is_present else Q()))
        else:
            criteria = Q()
        paginated_roll_call = pagination(RollCall, size, page, criteria)
        serializer = RollCallSerializer(paginated_roll_call, many=True)
        return Response(serializer.data + [{"size": size, "page": page}])

    def post(self, request):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            request.data["recorder_id"] = request.user.id
            serializer = RollCallSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)


class RollCallDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            roll_call = RollCall.objects.get(pk=pk)
            serializer = RollCallSerializer(roll_call)
            return Response(serializer.data)
        except RollCall.DoesNotExist:
            return Response({"error": "roll call not found"} ,status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            request.data["recorder_id"] = request.user.id
            roll_call = RollCall.objects.get(pk=pk)
            roll_call_data = RollCallUpdateSerializer(roll_call).data
            roll_call_data.update(request.data)
            serializer = RollCallUpdateSerializer(roll_call, data=roll_call_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except RollCall.DoesNotExist:
            return Response({"error": "roll call not found"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            roll_call = RollCall.objects.get(pk=pk)
            roll_call.delete()
            return Response({"massage": "roll call deleted"}, status=status.HTTP_204_NO_CONTENT)
        except RollCall.DoesNotExist:
            return Response({"error": "roll call not found"}, status=status.HTTP_404_NOT_FOUND)