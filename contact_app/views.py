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
            # ✅ Fetch data
            queryset = Contact.objects.all().values()

            if not queryset:
                return Response(
                    {"status": False, "message": "No data available"},
                    status=status.HTTP_404_NOT_FOUND
                )

            df = pd.DataFrame(list(queryset))

            # ✅ Add Serial Number
            df.insert(0, 'S. No', range(1, len(df) + 1))

            # ✅ Drop unnecessary fields
            if 'id' in df.columns:
                df.drop(columns=['id'], inplace=True)

            # ✅ Rename columns
            df.rename(columns={
                'name': 'Name',
                'email': 'Email',
                'mobile': 'Mobile Number',
                'subject': 'Subject',
                'message': 'Message',
                'created_at': 'Created At'
            }, inplace=True)

            # ✅ Handle missing values
            df.fillna('', inplace=True)

            # ✅ 🔥 FIX: Remove timezone from datetime (IMPORTANT)
            for col in df.columns:
                if pd.api.types.is_datetime64_any_dtype(df[col]):
                    df[col] = df[col].dt.tz_localize(None)

            # ✅ Create Excel buffer
            output = BytesIO()
            df.to_excel(output, index=False, engine='openpyxl')
            output.seek(0)

            # ✅ Load workbook for styling
            workbook = load_workbook(output)
            worksheet = workbook.active

            # ✅ Auto column width
            for column_cells in worksheet.columns:
                max_length = 0
                column_letter = column_cells[0].column_letter

                for cell in column_cells:
                    try:
                        if cell.value:
                            max_length = max(max_length, len(str(cell.value)))
                    except:
                        pass

                worksheet.column_dimensions[column_letter].width = max_length + 2

            # ✅ Bold header
            for cell in worksheet[1]:
                cell.font = Font(bold=True)

            # ✅ Save final file
            final_output = BytesIO()
            workbook.save(final_output)
            final_output.seek(0)

            # ✅ Response
            response = HttpResponse(
                final_output.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=contacts.xlsx'

            return response

        except Exception as e:
            return Response(
                {
                    "status": False,
                    "message": "Failed to export data",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


def home(request):
    return HttpResponse("API is running successfully")