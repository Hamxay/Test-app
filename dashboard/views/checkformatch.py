import random
import requests
from django.views import View
from django.http import JsonResponse
from dashboard.models import Contacts, Crushesdb
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

SENDGRID_API='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'


@method_decorator(csrf_exempt, name='dispatch')
class CheckForMatch(View):

    def check_for_match(self,submitter_email, crush_email):
        try:
            crush_ins=Crushesdb.objects.filter(submitter_email=crush_email,crush_email=submitter_email).first()
            return crush_ins
            
        except Exception as e:
            print(f"OperationalError occurred: {e}")
            return None
    
    def insert_new_match(self,submitter_email, crush_name, crush_email):
        try:
            contacts_db=Contacts.objects.filter(email=submitter_email).first()
            submitter_name=contacts_db.name

            Crushesdb.objects.get_or_create(
                submitter_name=submitter_name,
                submitter_email=submitter_email,
                crush_name=crush_name,
                crush_email=crush_email)
        
        except Exception as e:
            print(f"OperationalError occurred: {e}")
            return None
        
    # send email with subject and content
    def send_email(self,to_email, subject, content):
        from_email = 'standrewscupid@gmail.com'
        message = Mail(from_email=from_email, to_emails=to_email, subject=subject, html_content=content)
        try:
            sg = SendGridAPIClient(SENDGRID_API)
            response = sg.send(message)
            return
        except Exception as e:
            return None
        
    def post(self, request:requests) -> dict:
    
        fname=request.POST.get('fname')
        sname=request.POST.get('sname')
        emmaiil=request.POST.get('emmaiil')
        user_email = request.session.get('email')
        crush_ins=self.check_for_match(user_email,emmaiil)

        crush_name = f"{fname} {sname}"
        newcrush=self.insert_new_match(user_email,crush_name,emmaiil)
        
        if crush_ins:
            return JsonResponse({'congrats':'yes'}, safe=False)
        else:
            return JsonResponse({'congrats':'no'}, safe=False)
        
        

        
           
    