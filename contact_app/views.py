from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.http import HttpResponse

from .models import Contact
from .serializers import ContactSerializer
from .services import create_contact, generate_contacts_excel
from .utils import success_response, error_response

# ✅ REGISTER API
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = ContactSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            contact = create_contact(serializer.validated_data)

            return Response(
                success_response(
                    ContactSerializer(contact).data,
                    "User registered successfully"
                ),
            status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                error_response("Something went wrong", str(e)),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ✅ EXPORT EXCEL API (CLEAN VERSION)
class ExportExcelAPI(APIView):

    def get(self, request):
        try:
            queryset = Contact.objects.all()

            excel_file = generate_contacts_excel(queryset)

            if excel_file is None:
                return Response(
                    error_response("No data available"),
                    status=status.HTTP_404_NOT_FOUND
                )

            response = HttpResponse(
                excel_file.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=contacts.xlsx'

            return response

        except Exception as e:
            return Response(
                error_response("Failed to export data", str(e)),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ✅ HEALTH CHECK / HOME
def home(request):
    return HttpResponse("API is running successfully 🚀")