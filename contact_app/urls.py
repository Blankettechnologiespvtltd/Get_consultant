from django.urls import path
from .views import RegisterAPIView, ExportExcelAPI, home

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('export-excel/', ExportExcelAPI.as_view()),
    path('', home),
]
