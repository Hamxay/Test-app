from django.http import JsonResponse
from django.views import View
from django.db.models import Q
from dashboard.models import Contacts

class Results(View):
    def get(self, request, *args, **kwargs):
        term =  request.GET.get('q')
        all_contacts=Contacts.objects.filter(
            Q(name__icontains=term) | Q(email__icontains=term)
        )
        data = [{'id': contact.email, 'text': f'{contact.name} -- {contact.email}'} for contact in all_contacts]
        context = {
        'items': data,
        }
        return JsonResponse(context)