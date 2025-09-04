# urls.py
from django.urls import path
from .views import PersonalExportAPIView

urlpatterns = [
    path('personal/excel/', PersonalExportAPIView.as_view(), name='personal-excel'),
]