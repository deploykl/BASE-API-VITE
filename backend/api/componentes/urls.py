# urls.py
from django.urls import path
from .views import PersonalExportAPIView, PersonalExportCSVAPIView, PersonalExportPDFAPIView

urlpatterns = [
    path('personal/excel/', PersonalExportAPIView.as_view(), name='personal-excel'),
    path('personal/csv/', PersonalExportCSVAPIView.as_view(), name='personal-csv'),
    path('personal/pdf/', PersonalExportPDFAPIView.as_view(), name='personal-pdf'),
]