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
import traceback

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
        try:
            contacts = list(Contact.objects.all().values())

            if not contacts:
                return HttpResponse("No data available")

            df = pd.DataFrame(contacts)

            # Add Serial Number column
            df.insert(0, 'S. No', range(1, len(df) + 1))

            # Remove ID column if exists
            if 'id' in df.columns:
                df.drop(columns=['id'], inplace=True)

            # Rename columns
            df.rename(columns={
                'name': 'Name',
                'email': 'Email',
                'mobile': 'Mobile Number',
                'region': 'Region',
                'message': 'Message/Comments'
            }, inplace=True)

            df.fillna('', inplace=True)

            for col in df.select_dtypes(include=['datetime64[ns]', 'datetime64[ns, UTC]']).columns:
                df[col] = df[col].astype(str)

            buffer = BytesIO()
            df.to_excel(buffer, index=False, engine='openpyxl')
            buffer.seek(0)

            # Send response
            response = HttpResponse(
                buffer.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=contacts.xlsx'

            return response

        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=500)

def home(request):
    return HttpResponse("API is running successfully")