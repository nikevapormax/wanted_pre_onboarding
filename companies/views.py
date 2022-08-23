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
    
    # 채용공고 수정
    def put(self, request):
        old_recruitments = RecruitmentsModel.objects.get(id=request.data["id"])
        recruitments = RecruitmentsChangeSerializer(old_recruitments, data=request.data, partial=True)
        
        if recruitments.is_valid():
            recruitments.save()
            return Response(recruitments.data, status=status.HTTP_200_OK)
        
        return Response({"message" : "채용공고 수정 실패!"}, status=status.HTTP_400_BAD_REQUEST)

        