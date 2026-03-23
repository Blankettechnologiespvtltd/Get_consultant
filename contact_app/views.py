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
from openpyxl import load_workbook
from openpyxl.styles import Font

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
                'subject': 'Subject',
                'message': 'Message'
            }, inplace=True)

            df.fillna('', inplace=True)

            for col in df.select_dtypes(include=['datetime64[ns]', 'datetime64[ns, UTC]']).columns:
                df[col] = df[col].astype(str)

            buffer = BytesIO()
            df.to_excel(buffer, index=False, engine='openpyxl')
            buffer.seek(0)

            # Load workbook
            workbook = load_workbook(buffer)
            worksheet = workbook.active

            # ✅ Auto adjust column width
            for col in worksheet.columns:
                max_length = 0
                col_letter = col[0].column_letter

                for cell in col:
                    try:
                        if cell.value:
                            max_length = max(max_length, len(str(cell.value)))
                    except:
                        pass

                worksheet.column_dimensions[col_letter].width = max_length + 2

            # ✅ Bold header (optional but recommended)
            for cell in worksheet[1]:
                cell.font = Font(bold=True)

            # Save to new buffer
            new_buffer = BytesIO()
            workbook.save(new_buffer)
            new_buffer.seek(0)

            # Send response
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