from django.contrib import admin

from .models import Company as CompanyModel
from .models import Recruitments as RecruitmentsModel


admin.site.register(CompanyModel)
admin.site.register(RecruitmentsModel)