from .models import Contact

def get_all_contacts():
    return Contact.objects.all()