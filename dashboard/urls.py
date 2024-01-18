from django.urls import path

from dashboard.views import Dashboard, LoginView, CreateSession, MatcherView, CheckForMatch, Results

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('createsession', CreateSession.as_view(), name='createsession'),
    path('matcherview', MatcherView.as_view(), name='matcherview'),
    path('checkformatch', CheckForMatch.as_view(), name='checkformatch'),
    path('', Dashboard.as_view(), name='dashboard'),
    path('results', Results.as_view(), name='results'),
    
    
]
    
