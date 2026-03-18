from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ContactCreateAPI, ExportExcelAPI, home, ContactViewSet

router = DefaultRouter()
router.register(r'contacts', ContactViewSet)

urlpatterns = [
    path('register/', ContactCreateAPI.as_view()),
    path('export-excel/', ExportExcelAPI.as_view()),
    path('', home),
]

# 👇 IMPORTANT: add this line
urlpatterns += router.urls
