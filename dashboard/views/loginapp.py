import random
import requests
from django.views import View
from datetime import timedelta
from django.utils import timezone
from django.http import JsonResponse
from dashboard.models import Contacts, OTPAttempts
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from dashboard.messages import (TOO_MANY_ATTEMPTS)

SENDGRID_API='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'

# send verification code to email 
def send_verification_code(email):
    code = str(random.randint(100000, 999999))
    from_email = 'standrewscupid@gmail.com'
    message = Mail(from_email=from_email, to_emails=email, subject='Verification Code', html_content=f"Your verification code is: {code}")
    try:
        sg = SendGridAPIClient(SENDGRID_API)
        response = sg.send(message)
    except Exception as e:
        code=None
    return code

def get_user_attempts(email):
    try:
        user_attempts = OTPAttempts.objects.get(email=email)
        return user_attempts
    except OTPAttempts.DoesNotExist:
        return None

def handle_login_attempt(user_attempts):
    if user_attempts.attempts >= 5:
        time_since_latest_attempt = timezone.now() - user_attempts.latest_timestamp

        if time_since_latest_attempt < timezone.timedelta(hours=2):
            wait_time = timezone.timedelta(hours=2) - time_since_latest_attempt
            hours = int(wait_time.total_seconds() // 3600)
            minutes = int((wait_time.total_seconds() % 3600) // 60)
            wait_time = f"{hours} hours, {minutes} minutes"
            return wait_time

        else:
            user_attempts.attempts = 1
            user_attempts.latest_timestamp = timezone.now()
    else:
        user_attempts.attempts += 1
        user_attempts.latest_timestamp = timezone.now()

    user_attempts.save()
    return None


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):

    def get(self, request:requests) -> dict:
        user_email = request.session.get('email')
        if user_email:
            return redirect('/dashboard/matcherview')  
       
        return render(request, "login.html",{})
    
    def post(self, request:requests) -> dict:
    
        email=request.POST.get('email')
        contacts_db=Contacts.objects.filter(email=email)
        if contacts_db:
            # checking user attempts
            user_attempts = get_user_attempts(email)
            if user_attempts is not None:
                status = handle_login_attempt(user_attempts)
                if status:
                    return JsonResponse(
                        {
                            'user':0,
                            'code':'',
                            'messages': TOO_MANY_ATTEMPTS % {'time':status}
                        }
                    , safe=False)
            else:
                OTPAttempts.objects.create(email=email, attempts=1, first_attempt_time=timezone.now(), latest_timestamp=timezone.now())

            # send verification code to the user
            code=send_verification_code(email)
            return JsonResponse({'user':email,'code':code}, safe=False)
        else:
            return JsonResponse({'user':0,'code':''}, safe=False)
        

   
        
           
    