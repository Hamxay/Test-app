import requests
from django.views import View
from django.shortcuts import render,redirect


class Dashboard(View):

    def get(self, request:requests) -> dict:
        
        return render(request, "dashboard.html",{})
        
        
           
    