from django.urls import path
from companies import views


urlpatterns = [
    path("", views.CompaniesAPIView.as_view(), name="companies"),
]
