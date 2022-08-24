from reprlib import recursive_repr
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Recruitments as RecruitmentsModel
from .serializers import RecruitmentsSerializer
from .serializers import RecruitmentsChangeSerializer
from .serializers import RecruitmentsLookupSeriailizer
from .serializers import RecruitmentsDetailSerializer


class CompaniesAPIView(APIView):
    # 채용공고 조회
    def get(self, request):
        all_recruitments = RecruitmentsModel.objects.all()
        all_recruitments_data = RecruitmentsLookupSeriailizer(all_recruitments, many=True)
        
        return Response(all_recruitments_data.data, status=status.HTTP_200_OK)
    
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
        
        return Response(recruitments.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 채용공고 삭제
    def delete(self, request):
        try:
            recruitments = RecruitmentsModel.objects.get(id=request.data["id"])
            
            if recruitments:
                recruitments.delete()
                return Response({"message": "채용공고 삭제 성공!"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "채용공고가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
        

class RecruitmentsSearchView(APIView):
    # 검색어를 통한 채용공고 검색
    def get(self, request):
        param = request.query_params.get("search")
        
        if not param:
            return Response({"message" : "검색 결과가 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            if int(param) >= 500000:
                data = RecruitmentsModel.objects.filter(recruit_compensation__gte=int(param))

                if data.exists():
                    serialized_data = RecruitmentsLookupSeriailizer(data, many=True)
                    return Response(serialized_data.data, status=status.HTTP_200_OK)
                else:
                    return Response({"message" : "검색 결과가 없습니다."}, status=status.HTTP_404_NOT_FOUND)
            else:
                data = RecruitmentsModel.objects.filter(id=int(param))

                if data.exists():
                    serialized_data = RecruitmentsLookupSeriailizer(data, many=True)
                    return Response(serialized_data.data, status=status.HTTP_200_OK)
                else:
                    return Response({"message" : "검색 결과가 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        except:
            if RecruitmentsModel.objects.filter(company__company_name__icontains=param):
                data = RecruitmentsModel.objects.filter(company__company_name__icontains=param)
                serialized_data = RecruitmentsLookupSeriailizer(data, many=True)
                return Response(serialized_data.data, status=status.HTTP_200_OK)
            elif RecruitmentsModel.objects.filter(country__icontains=param):
                data = RecruitmentsModel.objects.filter(country__icontains=param)
                serialized_data = RecruitmentsLookupSeriailizer(data, many=True)
                return Response(serialized_data.data, status=status.HTTP_200_OK)
            elif RecruitmentsModel.objects.filter(region__icontains=param):
                data = RecruitmentsModel.objects.filter(region__icontains=param)
                serialized_data = RecruitmentsLookupSeriailizer(data, many=True)
                return Response(serialized_data.data, status=status.HTTP_200_OK)
            elif RecruitmentsModel.objects.filter(position__icontains=param):
                data = RecruitmentsModel.objects.filter(position__icontains=param)
                serialized_data = RecruitmentsLookupSeriailizer(data, many=True)
                return Response(serialized_data.data, status=status.HTTP_200_OK)
            elif RecruitmentsModel.objects.filter(skill__icontains=param):
                data = RecruitmentsModel.objects.filter(skill__icontains=param)
                serialized_data = RecruitmentsLookupSeriailizer(data, many=True)
                return Response(serialized_data.data, status=status.HTTP_200_OK)
            else:
                return Response({"message" : "검색 결과가 없습니다."}, status=status.HTTP_404_NOT_FOUND)
            

class RecruitmentsDetailView(APIView):
    # 채용공고 상세 페이지
    def get(self, request, id):
        recruitments = RecruitmentsModel.objects.get(id=id)
        recruitments_data = RecruitmentsDetailSerializer(recruitments)
        
        return Response(recruitments_data.data, status=status.HTTP_200_OK)