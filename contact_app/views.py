from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Contact
from .serializers import ContactSerializer
import pandas as pd
from django.http import HttpResponse
from io import BytesIO
from openpyxl import load_workbook
from openpyxl.styles import Font


# ✅ REGISTER API (NEW CLEAN VERSION)
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]   # 🔥 important (fixes CSRF issue)

    def post(self, request):
        try:
            serializer = ContactSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "status": True,
                        "message": "User registered successfully",
                        "data": serializer.data
                    },
                    status=status.HTTP_201_CREATED
                )

            return Response(
                {
                    "status": False,
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {
                    "status": False,
                    "message": "Something went wrong",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ✅ EXPORT EXCEL API (UNCHANGED)
class ExportExcelAPI(APIView):
    def get(self, request):
        try:
            contacts = list(Contact.objects.all().values())

            if not contacts:
                return HttpResponse("No data available")

            df = pd.DataFrame(contacts)

            df.insert(0, 'S. No', range(1, len(df) + 1))

            if 'id' in df.columns:
                df.drop(columns=['id'], inplace=True)

            df.rename(columns={
                'name': 'Name',
                'email': 'Email',
                'mobile': 'Mobile Number',
                'subject': 'Subject',
                'message': 'Message'
            }, inplace=True)

            df.fillna('', inplace=True)

            buffer = BytesIO()
            df.to_excel(buffer, index=False, engine='openpyxl')
            buffer.seek(0)

            workbook = load_workbook(buffer)
            worksheet = workbook.active

            for col in worksheet.columns:
                max_length = 0
                col_letter = col[0].column_letter

                for cell in col:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))

                worksheet.column_dimensions[col_letter].width = max_length + 2

            for cell in worksheet[1]:
                cell.font = Font(bold=True)

            new_buffer = BytesIO()
            workbook.save(new_buffer)
            new_buffer.seek(0)

            response = HttpResponse(
                new_buffer.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=contacts.xlsx'

            return response

        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=500)


def home(request):
    return HttpResponse("API is running successfully")