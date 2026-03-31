import pandas as pd
from io import BytesIO
from openpyxl import load_workbook
from openpyxl.styles import Font
from .models import Contact
import logging

logger = logging.getLogger(__name__)


def create_contact(validated_data):
    return Contact.objects.create(**validated_data)


def generate_contacts_excel(queryset):
    try:
        df = pd.DataFrame(list(queryset.values()))

        if df.empty:
            return None

        df.insert(0, 'S. No', range(1, len(df) + 1))

        if 'id' in df.columns:
            df.drop(columns=['id'], inplace=True)

        if 'created_at' in df.columns:
            df['created_at'] = df['created_at'].astype(str)

        df.rename(columns={
            'name': 'Name',
            'email': 'Email',
            'mobile': 'Mobile Number',
            'subject': 'Subject',
            'message': 'Message',
            'created_at': 'Created At'
        }, inplace=True)

        df.fillna('', inplace=True)

        output = BytesIO()
        df.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)

        workbook = load_workbook(output)
        worksheet = workbook.active

        for cell in worksheet[1]:
            cell.font = Font(bold=True)

        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter

            for cell in column:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))

            worksheet.column_dimensions[column_letter].width = max_length + 2

        final_output = BytesIO()
        workbook.save(final_output)
        final_output.seek(0)

        return final_output

    except Exception:
        logger.error("Excel generation failed", exc_info=True)
        return None