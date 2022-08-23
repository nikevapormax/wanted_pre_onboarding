from django.db import models


class Company(models.Model):
    company_name = models.CharField("회사이름", max_length=40)
    
    def __str__(self):
        return self.company_name


class Recruitments(models.Model):
    company = models.ForeignKey(Company, verbose_name="회사명", on_delete=models.CASCADE)
    position = models.CharField("채용포지션", max_length=30)
    recruit_compensation = models.IntegerField("채용보상금")
    contents = models.TextField("채용내용")
    skill = models.CharField("기술", max_length=30)

    def __str__(self):
        return f"{self.company.company_name} -> {self.position} ({self.skill})"