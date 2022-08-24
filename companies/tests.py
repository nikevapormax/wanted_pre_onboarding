from django.urls import reverse
from rest_framework.test import APITestCase

from .models import Company as CompanyModel
from .models import Recruitments as RecruitmentsModel
class RecruitmentsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        company_data = ["배달의민족", "요기요", "삼성", "엘지"]
        for company in company_data:
            cls.company = CompanyModel.objects.create(company_name=company)

    # 채용공고 등록 테스트 (성공)
    def test_register_recruitments(self):
        url = reverse("companies")
        data = {
            "company" : 1,
            "country" : "한국",
            "region" : "강남",
            "position" : "백엔드 시니어 개발자",
            "recruit_compensation" : "500000",
            "contents" : "배달의민족에서 백엔드 시니어 개발자를 채용합니다. 많관부!",
            "skill" : "Django",
        }
        data_2 = {
            "company" : 4,
            "country" : "한국",
            "region" : "마포",
            "position" : "백엔드 주니어 개발자",
            "recruit_compensation" : "1000000",
            "contents" : "엘지에서 백엔드 주니어 개발자를 채용합니다. 많관부!",
            "skill" : "Python",
        }
        data_3 = {
            "company" : 3,
            "country" : "한국",
            "region" : "수원",
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
        
    # 채용공고 등록 테스트 (실패)
    def test_register_recruitments_not_enough_info(self):
        url = reverse("companies")
        data = {
            "company" : "",
            "country" : "",
            "region" : "강남",
            "position" : "백엔드 시니어 개발자",
            "recruit_compensation" : "500000",
            "contents" : "배달의민족에서 백엔드 시니어 개발자를 채용합니다. 많관부!",
            "skill" : "Django",
        }
        data_2 = {
            "company" : 2,
            "country" : "한국",
            "region" : "",
            "position" : "",
            "recruit_compensation" : "1000000",
            "contents" : "엘지에서 백엔드 주니어 개발자를 채용합니다. 많관부!",
            "skill" : "Python",
        }
        data_3 = {
            "company" : 3,
            "country" : "한국",
            "region" : "강남",
            "position" : "프론트엔드 시니어 개발자",
            "recruit_compensation" : "",
            "contents" : "",
            "skill" : "Vue.js",
        }
        
        response = self.client.post(url, data)
        response_2 = self.client.post(url, data_2)
        response_3 = self.client.post(url, data_3)
        
        self.assertEqual(response.data["company"][0], "This field may not be null.")
        self.assertEqual(response.data["country"][0], "This field may not be blank.")
        self.assertEqual(response_2.data["position"][0], "This field may not be blank.")
        self.assertEqual(response_2.data["region"][0], "This field may not be blank.")
        self.assertEqual(response_3.data["recruit_compensation"][0], "A valid integer is required.")
        self.assertEqual(response_3.data["contents"][0], "This field may not be blank.")


class RecruitmentsReviseOrDeleteTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        company_data = ["배달의민족", "요기요"]
        for company in company_data:
            cls.company = CompanyModel.objects.create(company_name=company)
        
        cls.recruitments = RecruitmentsModel.objects.create(
            company=CompanyModel.objects.get(id=1),
            country="한국",
            region="강남",
            position="프론트엔드 주니어 개발자",
            recruit_compensation=500000,
            contents="배달의민족에서 프론트엔드 주니어 개발자를 채용합니다!",
            skill="Vue.js"
        )
        cls.recruitments_1 = RecruitmentsModel.objects.create(
            company=CompanyModel.objects.get(id=2),
            country="한국",
            region="선릉",
            position="백엔드 주니어 개발자",
            recruit_compensation=1500000,
            contents="요기요에서 백엔드 주니어 개발자를 채용합니다!",
            skill="Python"
        )

    # 채용공고 수정 테스트 (성공)
    def test_revise_register(self):
        url = reverse("companies")
        data = {
            "id" : 1,
            "company" : 1,
            "country" : "미국",
            "region" : "실리콘밸리",
            "position" : "프론트엔드 시니어 개발자",
            "recruit_compensation" : 500000,
            "contents" : "배달의민족에서 프론트엔드 시니어 개발자를 채용합니다. 많관부!",
            "skill" : "Vue.js",
        }
        data_1 = {
            "id" : 2,
            "company" : 2,
            "country" : "한국",
            "region" : "강남",
            "position" : "백엔드 주니어 개발자",
            "recruit_compensation" : 5000000000,
            "contents" : "요기요에서 백엔드 시니어 개발자를 채용합니다. 많관부!",
            "skill" : "Django",
        }
        
        response = self.client.put(url, data)
        response_1 = self.client.put(url, data_1)
        
        self.assertEqual(response.data["country"], "미국")
        self.assertEqual(response.data["region"], "실리콘밸리")
        self.assertEqual(response.data["position"], "프론트엔드 시니어 개발자")
        self.assertEqual(response.data["contents"], "배달의민족에서 프론트엔드 시니어 개발자를 채용합니다. 많관부!")
        self.assertEqual(response_1.data["region"], "강남")
        self.assertEqual(response_1.data["recruit_compensation"], 5000000000)
        self.assertEqual(response_1.data["contents"], "요기요에서 백엔드 시니어 개발자를 채용합니다. 많관부!")
        self.assertEqual(response_1.data["skill"], "Django")
        
    # 채용공고 수정 테스트 (실패)
    def test_revise_register_fail(self):
        url = reverse("companies")
        data = {
            "id" : 1,
            "company" : 1,
            "country" : "한국남아프리카공화국미국중국크로아티아영국프랑스포르투갈그린란드이탈리아",
            "region" : "강남",
            "position" : "프론트엔드 시니어 개발자 개발자 개발자 개발자 개발자 개발자 개발자",
            "recruit_compensation" : 500000,
            "contents" : "배달의민족에서 프론트엔드 시니어 개발자를 채용합니다. 많관부!",
            "skill" : "Vue.js",
        }
        data_1 = {
            "id" : 2,
            "company" : 2,
            "country" : "한국",
            "region" : "강남강서강북마포중구중랑구서대문구안양의왕수원인덕원비산동과천시은평구",
            "position" : "백엔드 주니어 개발자",
            "recruit_compensation" : 50000000000000000,
            "contents" : "요기요에서 백엔드 시니어 개발자를 채용합니다. 많관부!",
            "skill" : "DjangoDjangoDjangoDjangoDjangoDjangoDjangoDjangoDjango",
        }
        
        response = self.client.put(url, data)
        response_1 = self.client.put(url, data_1)
        
        self.assertEqual(response.data["country"][0], "Ensure this field has no more than 20 characters.")
        self.assertEqual(response.data["position"][0], "Ensure this field has no more than 30 characters.")
        self.assertEqual(response_1.data["region"][0], "Ensure this field has no more than 15 characters.")
        self.assertEqual(response_1.data["skill"][0], "Ensure this field has no more than 30 characters.")
        
    # 채용공고 삭제 테스트 (성공)
    def test_delete_register(self):
        url = reverse("companies")
        data = {
            "id" : 1
        }
        data_1 = {
            "id" : 2
        }
        
        response = self.client.delete(url, data)
        response_1 = self.client.delete(url, data_1)
        
        self.assertEqual(response.data["message"], "채용공고 삭제 성공!")
        self.assertEqual(response_1.data["message"], "채용공고 삭제 성공!")

    # 채용공고 삭제 테스트 (실패)
    def test_delete_register(self):
        url = reverse("companies")
        data = {
            "id" : 3
        }
        data_1 = {
            "id" : 10
        }
        
        response = self.client.delete(url, data)
        response_1 = self.client.delete(url, data_1)
        
        self.assertEqual(response.data["message"], "채용공고가 존재하지 않습니다.")
        self.assertEqual(response_1.data["message"], "채용공고가 존재하지 않습니다.")