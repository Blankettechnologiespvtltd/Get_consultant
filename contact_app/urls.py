from django.urls import path
from .views import ContactCreateAPI, ExportExcelAPI, home

urlpatterns = [
    path('register/', ContactCreateAPI.as_view()),
    path('export-excel/', ExportExcelAPI.as_view()),
    path('', home),
]
