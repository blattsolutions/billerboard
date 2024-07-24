"""
URL configuration for stb_billerboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('createhubspotcandidate/', views.createhubspotcandidate, name='createhubspotcandidate'),
    path('sendhubspotcandidate/', views.sendhubspotcandidate, name='sendhubspotcandidate'),
    path('createhubspotunternehmen/', views.createhubspotunternehmen, name='createhubspotunternehmen'),
    path('sendhubspotunternehmen/', views.sendhubspotunternehmen, name='sendhubspotunternehmen'),



    path('team/', views.team, name='team'),
    
    
    path('interviewboard/add/', views.addivboard, name='addivboard'),
    path('interviewboard/alle', views.alleivboards, name='alleivboards'),
    path('interviewboard/gesamt/', views.ivboardall, name='ivboardall'),
    path('interviewboard/<int:ivboard_id>', views.ivboard, name='ivboard'),
    path('interviewboard/updateivtoday/<int:entry_pk>', views.updateivtoday, name='updateivtoday'),
    path('interviewboard/updateivthisweek/<int:entry_pk>', views.updateivthisweek, name='updateivthisweek'),
    path('interviewboard/updateivnextweek/<int:entry_pk>', views.updateivnextweek, name='updateivnextweek'),
    path('interviewboard/updateoffer/<int:entry_pk>', views.updateoffer, name='updateoffer'),
    path('interviewboard/updaterevenue/<int:entry_pk>', views.updaterevenue, name='updaterevenue'),

    path('prozesse/', views.prozessboard, name='prozessboard'),
    path('prozesse/schliessen/won/<int:prozess_id>', views.prozess_schliessen_won, name='prozess_schliessen_won'),
    path('prozesse/schliessen/lost/<int:prozess_id>', views.prozess_schliessen_lost, name='prozess_schliessen_lost'),
    path('prozesse/alt/', views.prozessboard_alte_prozesse, name='prozessboard_alte_prozesse'),
    path('prozesse/createoffer/<int:board_id>', views.createoffer, name='createoffer'),
    path('prozesse/closeoffer/lost/<int:offer_id>', views.offer_schliessen_lost, name='offer_schliessen_lost'),
    path('prozesse/closeoffer/won/<int:offer_id>', views.offer_schliessen_won, name='offer_schliessen_won'),
    

    path('toolkosten/', views.toolrechnung, name='toolrechnung'),
    path('toolkosten/bezahlen/<int:rechnung_id>', views.toolkostenrechnung_bezahlt, name='toolkostenrechnung_bezahlt'),
    path('einzahlung/', views.einzahlung, name='einzahlung'),
    
    path('partnerliste/', views.partnerliste, name='partnerliste'),
    path('blackliste/', views.blackliste, name='blackliste'),
    path('deals/einreichen/', views.deal_einreichen, name='deal_einreichen'),
    path('deals/genehmigen/<int:deal_id>', views.deal_genehmigen, name='deal_genehmigen'),
    path('deals/storno/<int:deal_id>', views.deal_storno, name='deal_storno'), 
    path('deals/dateneinreichen/<int:deal_id>', views.deal_daten_einreichen, name='deal_daten_einreichen'),
    path('deals/', views.deals, name='deals'),
    path('deals/user/<int:user_id>/', views.deals_user, name='deals_user'),
    path('deals/dealdaten/<int:deal_id>', views.datenzip, name='datenzip'),

    path('profil/rechnungsdaten/', views.rechnungsdaten, name='rechnungsdaten'),
    path('rangliste/', views.rang_overview, name='rang_overview'),

    path('htmx/topperformer/<int:year>/<int:month>', views.top_performers_month, name='top_performers_month'),
    path('htmx/walloffame/', views.wall_of_fame, name='wall_of_fame'),

] 