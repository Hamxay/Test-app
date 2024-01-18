import requests
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class CreateSession(View):

    def post(self, request:requests) -> dict:
        session=request.POST.get('createsession')
        useremail=request.POST.get('useremail')
        
        if session=='1':
            request.session['email'] = useremail
            return JsonResponse({'session':1}, safe=False)
        else:
            print(20)
            return JsonResponse({'session':0}, safe=False)
        

   
        
           
    