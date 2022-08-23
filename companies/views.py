from reprlib import recursive_repr
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Recruitments as RecruitmentsModel
from .serializers import RecruitmentsSerializer
from .serializers import RecruitmentsChangeSerializer
from companies import serializers

class CompaniesAPIView(APIView):
    # 채용공고 등록
    def post(self, request):
        recruitments = RecruitmentsSerializer(data=request.data)

        if recruitments.is_valid():
            recruitments.save()
            return Response(recruitments.data, status=status.HTTP_200_OK)
        
        return Response(recruitments.errors, status=status.HTTP_400_BAD_REQUEST)
    