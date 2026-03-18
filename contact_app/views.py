from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Contact
from .serializers import ContactSerializer
import pandas as pd
from django.http import HttpResponse
from io import BytesIO
from rest_framework.viewsets import ModelViewSet

# API to Save Data
class ContactCreateAPI(APIView):
    def post(self, request):
        serializer = ContactSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Data saved successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API to Export Excel

class ExportExcelAPI(APIView):
    def get(self, request):

        contacts = Contact.objects.all().values()
        df = pd.DataFrame(contacts)

        # Add Serial Number
        df.insert(0, 'S. No', range(1, len(df) + 1))
        df.drop(columns=['id'], inplace=True)

        # Rename columns
        df.rename(columns={
            'name': 'Name',
            'email': 'Email',
            'mobile': 'Mobile Number',
            'region': 'Region',
            'message': 'Message/Comments'
        }, inplace=True)

        buffer = BytesIO()
        df.to_excel(buffer, index=False)
        buffer.seek(0)

        response = HttpResponse(
            buffer,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        response['Content-Disposition'] = 'attachment; filename=contacts.xlsx'
        return response

class ContactViewSet(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

def home(request):
    return HttpResponse("API is running successfully")