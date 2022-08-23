from django.urls import reverse
from rest_framework.test import APITestCase

from .models import Company as CompanyModel
class RecruitmentsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        company_data = ["배달의민족", "요기요", "삼성", "엘지"]
        for company in company_data:
            cls.company = CompanyModel.objects.create(company_name=company)
        
        cls.company.save()
    
    # 채용공고 등록 테스트 (성공)
    def test_register_recruitments(self):
        url = reverse("companies")
        data = {
            "company" : 1,
            "position" : "백엔드 시니어 개발자",
            "recruit_compensation" : "500000",
            "contents" : "배달의민족에서 백엔드 시니어 개발자를 채용합니다. 많관부!",
            "skill" : "Django",
        }
        data_2 = {
            "company" : 4,
            "position" : "백엔드 주니어 개발자",
            "recruit_compensation" : "1000000",
            "contents" : "엘지에서 백엔드 주니어 개발자를 채용합니다. 많관부!",
            "skill" : "Python",
        }
        data_3 = {
            "company" : 3,
            "position" : "프론트엔드 시니어 개발자",
            "recruit_compensation" : "500000",
            "contents" : "삼성에서 프론트엔드 시니어 개발자를 채용합니다. 많관부!",
            "skill" : "Vue.js",
        }
        
        response = self.client.post(url, data)
        response_2 = self.client.post(url, data_2)
        response_3 = self.client.post(url, data_3)
        
        self.assertEqual(response.data["company"], 1)
        self.assertEqual(response.data["skill"], "Django")
        self.assertEqual(response_2.data["company"], 4)
        self.assertEqual(response_2.data["recruit_compensation"], 1000000)
        self.assertEqual(response_3.data["company"], 3)
        self.assertEqual(response_3.data["contents"], "삼성에서 프론트엔드 시니어 개발자를 채용합니다. 많관부!")
