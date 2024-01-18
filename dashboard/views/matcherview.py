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



@method_decorator(csrf_exempt, name='dispatch')
class MatcherView(View):

    def get(self, request:requests) -> dict:
        user_email = request.session.get('email')
        if user_email is None:
            return redirect('/dashboard/login')  # Replace 'your_redirect_url' with the actual URL


        all_submitted_crush=Crushesdb.objects.filter(submitter_email=user_email)
        you_crushed_emails = list(Crushesdb.objects.filter(crush_email=user_email).values_list('submitter_email', flat=True))
        crushed_count=Crushesdb.objects.filter(crush_email=user_email).count
        
        login_crush_table_list=[]
        for crushed in all_submitted_crush:
            tmpdic={}
            tmpdic['crush_name']=crushed.crush_name
            tmpdic['crush_email']=crushed.crush_email[:40]
            if crushed.crush_email in you_crushed_emails:
                tmpdic['matched']='yes'
            else:
                tmpdic['matched']='no'
            
            login_crush_table_list.append(tmpdic)

        # all contacts for select dropdown
        all_contacts=Contacts.objects.all()

        return render(request, "matcher.html",{'crushed_count':crushed_count,'user_email':user_email,'login_crush_table_list':login_crush_table_list,'all_contacts':all_contacts})
    

    def extract_contact_details(self,dropdownselectemail):

        if not dropdownselectemail:
            return '', '', ''
        
        contactsdb=Contacts.objects.filter(email=dropdownselectemail).first()
        name=contactsdb.name
        name_words = name.split()
        fname = name_words[0] if name_words else ''
        sname = ' '.join(name_words[1:]) if len(name_words) > 1 else ''

        return fname,sname,dropdownselectemail

    def post(self, request:requests) -> dict:
    
        dropdownselectemail=request.POST.get('dropdownselectemail')
        fname,sname,email=self.extract_contact_details(dropdownselectemail)
        return JsonResponse({'fname':fname,'sname':sname,'email':email}, safe=False)
        
   
        
           
    