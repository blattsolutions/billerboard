import zipfile
from django.shortcuts import get_object_or_404, render, redirect
import calendar
from userauth.models import Profile, RangHistory, RechnungsDaten
from .models import DailySurvey, DailySurveyAnswer, DailySurveyQuestion, Deal, Kontakt, Kandidat, Offer, Tool, ToolKostenRechnung, Unternehmen, SalesStufe, ProvisionLayer, Share, Einzahlung, PartnerUnternehmen, BlacklistUnternehmen, DealDaten, Umsatzziel, InterviewBoard, InterviewBoardEntry, ProzessEntry
from django.utils import timezone
import names
import randomname
import random
from phone_gen import PhoneNumber
from faker import Faker
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import AddUserToInvoice, DealForm, OfferEntryForm, DealDatenForm, EinzahlungsForm, PartnerListenForm, BlackListenForm, KandidatHubspotForm, ProzessEntryForm, RechnungsDatenForm, ToolKostenRechnungForm, UnternehmenHubspotForm, DealDatenUploadForm, InterviewBoardForm, AddMemberToBoardForm
from django.contrib import messages
from dateutil.relativedelta import relativedelta
from userauth.tasks import calculate_rang
<<<<<<< HEAD
from django.http import HttpResponse, JsonResponse
=======
from django.http import HttpResponse,JsonResponse
>>>>>>> 1836f65e4abd7e4feb2cd7799eab2ad70fcb4096
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import locale
from django.db.models import Q
from .tasks import daily_iv_reset, daily_bonding_mail_check
# Beweise für Deal
# --> AGB bestätigt
# --> Vertragsunterschrift
# --> Dokumente hochladen
# --> Rechnungsnummerrechts
# --> Dashboard switch Teams vs Einzeln
# --> Jahresübersicht

# Create your views here.


@login_required()
def dashboard(request):
    try:
        umsatzziel_monat = Umsatzziel.objects.filter(date__month=timezone.now().month).filter(date__year=timezone.now().year).first()
        
        umsatzziel_jah_obj = Umsatzziel.objects.filter(date__year=timezone.now().year)
        umsatzziel_jahr = 0
        for u in umsatzziel_jah_obj:
            umsatzziel_jahr += u.amount
        
        last_10_deals = Deal.objects.all().order_by('-deal_closed_at')[:50]
        deals_this_month = Deal.objects.filter(
            deal_closed_at__month=timezone.now().month)
        last_month = timezone.now() - relativedelta(months=1)
        deals_last_month = Deal.objects.filter(deal_closed_at__month=last_month.month, deal_closed_at__year=last_month.year)
        deals_this_year = Deal.objects.filter(deal_closed_at__year=timezone.now().year)
        deals_last_year = Deal.objects.filter(deal_closed_at__year=timezone.now().year-1)
        revenue_this_month = 0
        revenue_last_month = 0
        revenue_this_year = 0
        revenue_last_year = 0
        for deal in deals_this_month:
            revenue_this_month += deal.amount
        for deal in deals_last_month:
            revenue_last_month += deal.amount
        for deal in deals_this_year:
            revenue_this_year += deal.amount
        for deal in deals_last_year:
            revenue_last_year += deal.amount
        difference_deal_revenue = revenue_this_month - revenue_last_month
        difference_deal_count = deals_this_month.count() - deals_last_month.count()
        difference_deal_year = revenue_this_year - revenue_last_year
        umsatz_engineering = 0
        umsatz_it = 0
        umsatz_finance = 0
        prozent_engineering = 0
        prozent_it = 0
        prozent_finance = 0
        userdict = {}
        anzahl_engineering = 0
        anzahl_finance = 0
        anzahl_it = 0
        deals_engineering = 0
        deals_it = 0
        deals_finance = 0
        for u in User.objects.all():
            if u.profile.abteilung:
                if u.profile.abteilung.name == 'Engineering':
                    anzahl_engineering += 1
                if u.profile.abteilung.name == 'IT':
                    anzahl_it += 1
                if u.profile.abteilung.name == 'Finance':
                    anzahl_finance += 1


        for d in deals_this_year:
            abteilung = d.abteilung
            if abteilung:
                if abteilung.name == 'Engineering':
                    umsatz_engineering += d.amount
                    deals_engineering += 1
                if abteilung.name == 'IT':
                    umsatz_it += d.amount
                    deals_it += 1
                if abteilung.name == 'Finance':
                    umsatz_finance += d.amount
                    deals_finance += 1
                if abteilung.name == 'Legal':
                    umsatz_finance += d.amount
                    deals_finance += 1
            if not d.user in userdict:
                if  d.shares():
                    rev = d.amount
                    for s in d.shares():
                        rev -= (d.amount * s.prozente/100)
                    userdict[d.user] = {'revenue': rev, 'deals': 1}
                else:
                    userdict[d.user] = {'revenue': d.amount, 'deals': 1}
            else:
                if d.shares():
                    rev = d.amount
                    for s in d.shares():
                        rev -= (d.amount * s.prozente/100)
                    userdict[d.user]['revenue'] += rev
                    userdict[d.user]['deals'] += 1
                else:
                    userdict[d.user]['revenue'] += d.amount
                    userdict[d.user]['deals'] += 1
        for d in deals_this_year:
            rev = d.amount
            for share in d.shares():
                if not share.user in userdict:
                    userdict[share.user] = {'revenue': 0, 'deals': 0}
                userdict[share.user]['revenue'] += (d.amount * share.prozente/100)
                userdict[share.user]['deals'] += 1

        # userdict = sorted(userdict, key=lambda x: (userdict[x]['revenue'], userdict[x]['count'])).reverse()
        
        userdict = dict(
            sorted(userdict.items(), key=lambda x: x[1]['revenue'], reverse=True))


    
        prozent_engineering = (umsatz_engineering/revenue_this_year)*100
        prozent_it = (umsatz_it/revenue_this_year)*100
        prozent_finance = (umsatz_finance/revenue_this_year)*100
        prokopf_engineering = umsatz_engineering/anzahl_engineering
        #daily_bonding_mail_check.delay()
        umsatzziel_monat = Umsatzziel.objects.filter(date__month=timezone.now().month).filter(date__year=timezone.now().year).first()
        
        umsatzziel_jah_obj = Umsatzziel.objects.filter(date__year=timezone.now().year)
        umsatzziel_jahr = 0
        for u in umsatzziel_jah_obj:
            umsatzziel_jahr += u.amount
        
        last_10_deals = Deal.objects.all().order_by('-deal_closed_at')[:50]
        deals_this_month = Deal.objects.filter(
            deal_closed_at__month=timezone.now().month)
        last_month = timezone.now() - relativedelta(months=1)
        deals_last_month = Deal.objects.filter(deal_closed_at__month=last_month.month, deal_closed_at__year=last_month.year)
        deals_this_year = Deal.objects.filter(deal_closed_at__year=timezone.now().year)
        deals_last_year = Deal.objects.filter(deal_closed_at__year=timezone.now().year-1)
        revenue_this_month = 0
        revenue_last_month = 0
        revenue_this_year = 0
        revenue_last_year = 0
        for deal in deals_this_month:
            revenue_this_month += deal.amount
        for deal in deals_last_month:
            revenue_last_month += deal.amount
        for deal in deals_this_year:
            revenue_this_year += deal.amount
        for deal in deals_last_year:
            revenue_last_year += deal.amount
        difference_deal_revenue = revenue_this_month - revenue_last_month
        difference_deal_count = deals_this_month.count() - deals_last_month.count()
        difference_deal_year = revenue_this_year - revenue_last_year
        umsatz_engineering = 0
        umsatz_it = 0
        umsatz_finance = 0
        prozent_engineering = 0
        prozent_it = 0
        prozent_finance = 0
        userdict = {}
        anzahl_engineering = 0
        anzahl_finance = 0
        anzahl_it = 0
        deals_engineering = 0
        deals_it = 0
        deals_finance = 0
        for u in User.objects.all():
            if u.profile.abteilung:
                if u.profile.abteilung.name == 'Engineering':
                    anzahl_engineering += 1
                if u.profile.abteilung.name == 'IT':
                    anzahl_it += 1
                if u.profile.abteilung.name == 'Finance':
                    anzahl_finance += 1


        for d in deals_this_year:
            abteilung = d.abteilung
            if abteilung:
                if abteilung.name == 'Engineering':
                    umsatz_engineering += d.amount
                    deals_engineering += 1
                if abteilung.name == 'IT':
                    umsatz_it += d.amount
                    deals_it += 1
                if abteilung.name == 'Finance':
                    umsatz_finance += d.amount
                    deals_finance += 1
            if not d.user in userdict:
                if  d.shares():
                    rev = d.amount
                    for s in d.shares():
                        rev -= (d.amount * s.prozente/100)
                    userdict[d.user] = {'revenue': rev, 'deals': 1}
                else:
                    userdict[d.user] = {'revenue': d.amount, 'deals': 1}
            else:
                if d.shares():
                    rev = d.amount
                    for s in d.shares():
                        rev -= (d.amount * s.prozente/100)
                    userdict[d.user]['revenue'] += rev
                    userdict[d.user]['deals'] += 1
                else:
                    userdict[d.user]['revenue'] += d.amount
                    userdict[d.user]['deals'] += 1
        for d in deals_this_year:
            rev = d.amount
            for share in d.shares():
                if not share.user in userdict:
                    userdict[share.user] = {'revenue': 0, 'deals': 0}
                userdict[share.user]['revenue'] += (d.amount * share.prozente/100)
                userdict[share.user]['deals'] += 1

        # userdict = sorted(userdict, key=lambda x: (userdict[x]['revenue'], userdict[x]['count'])).reverse()
        
        userdict = dict(
            sorted(userdict.items(), key=lambda x: x[1]['revenue'], reverse=True))


    
        prozent_engineering = (umsatz_engineering/revenue_this_year)*100
        prozent_it = (umsatz_it/revenue_this_year)*100
        prozent_finance = (umsatz_finance/revenue_this_year)*100
        prokopf_engineering = umsatz_engineering/anzahl_engineering
        try:
            prokopf_it = umsatz_it/anzahl_it
        except:
            prokopf_it = 0
        prokopf_finance = umsatz_finance/anzahl_finance
        durchschnitt_engineering = umsatz_engineering / deals_engineering
        try:
            durchschnitt_it = umsatz_it / deals_it
        except:
            durchschnitt_it = 0
        durchschnitt_finance = umsatz_finance / deals_finance
        top3_performers = list(userdict.items())[:3]
        rest_performers = dict(list(userdict.items())[3:])
        mein_kontostand = 0
        for deal in Deal.objects.all():
            if deal.user == request.user:
                mein_kontostand += deal.amount
        
        prozent_monat = (revenue_this_month/umsatzziel_monat.amount)*100
        prozent_jahr = (revenue_this_year/umsatzziel_jahr)*100
        if ToolKostenRechnung.objects.filter(rechnung_fuer=request.user).filter(bezahlt=False).exists():
            messages.warning(request, 'Sie haben noch offene Rechnungen für Toolkosten!')

        # message modal congrats for new deals
 
        locale.setlocale(locale.LC_ALL, 'de_DE')
        
        return render(request, 'billerboard/dashboard.html', {'last_10_deals': last_10_deals,
                                                            'revenue_this_month': revenue_this_month,
                                                            'revenue_last_month': revenue_last_month,
                                                            'deals_this_month': deals_this_month.count(),
                                                            'deals_last_month': deals_last_month.count(),
                                                            'difference_deal_revenue': difference_deal_revenue,
                                                            'difference_deal_count': difference_deal_count,
                                                            'difference_deal_year': difference_deal_year,
                                                            'revenue_this_year': revenue_this_year,
                                                            'revenue_last_year': revenue_last_year,
                                                            'top3_performers': top3_performers,
                                                            'rest_performers': rest_performers,
                                                            'mein_kontostand': mein_kontostand,
                                                                'umsatzziel_monat': umsatzziel_monat,
                                                                'prozent_monat': prozent_monat,
                                                                'prozent_jahr': prozent_jahr,
                                                                'umsatzziel_jahr': umsatzziel_jahr,
                                                                'umsatz_engineering': umsatz_engineering,
                                                                'umsatz_it': umsatz_it,
                                                                'umsatz_finance': umsatz_finance,
                                                                'prozent_engineering': prozent_engineering,
                                                                'prozent_it': prozent_it,
                                                                'prozent_finance': prozent_finance,
                                                                'prokopf_engineering': prokopf_engineering,
                                                                'prokopf_it': prokopf_it,
                                                                'prokopf_finance': prokopf_finance,
                                                                'anzahl_engineering': anzahl_engineering,
                                                                'anzahl_it': anzahl_it,
                                                                'anzahl_finance': anzahl_finance,
                                                                'durchschnitt_engineering': durchschnitt_engineering,
                                                                'durchschnitt_it': durchschnitt_it,
                                                                'durchschnitt_finance': durchschnitt_finance,
                                                                
                                                                
                                                            })
    except:
        messages.add_message(request, messages.ERROR, 'CONGRATULATIONS', 'CONGRATULATIONS')
        return render(request, 'billerboard/dashboard.html')

@login_required
def top_performers_month(request, month,year):
    if request.htmx:
        if month == 0 and year == 0:
            month = timezone.now().month
            year = timezone.now().year
        deals_this_month = Deal.objects.filter(
        deal_closed_at__month=month).filter(deal_closed_at__year=year)
        userdictmonth = {}
        gesamt = 0
        for d in deals_this_month:
      
            gesamt += d.amount
            if not d.user in userdictmonth:
                userdictmonth[d.user] = {'revenue': 0, 'deals': 0}
            rev = d.amount
            if  d.shares():    
                for s in d.shares():
                    rev -= (d.amount * s.prozente/100)
               
  
            userdictmonth[d.user]['revenue'] += rev
            userdictmonth[d.user]['deals'] += 1
        for d in deals_this_month:
            rev = d.amount
            for share in d.shares():
           
                if not share.user in userdictmonth:
                    userdictmonth[share.user] = {'revenue': 0, 'deals': 0}
                userdictmonth[share.user]['revenue'] += (d.amount * share.prozente/100)
                userdictmonth[share.user]['deals'] += 1

        # userdict = sorted(userdict, key=lambda x: (userdict[x]['revenue'], userdict[x]['count'])).reverse()
        userdictmonth = dict(
        sorted(userdictmonth.items(), key=lambda x: x[1]['revenue'], reverse=True))
        
        nextmonth = month+1
        nextyear = year
        prevmonth = month - 1
        prevyear = year
        if prevmonth == 0:
            prevmonth = 12
            prevyear = year-1
        if nextmonth == 13:
            nextmonth = 1
            nextyear = year+1
        
        locale.setlocale(locale.LC_ALL, 'de_DE')
    
        return render(request, 'billerboard/partials/top_performer_month_partial.html',{
            'userdictmonth': userdictmonth,
            'prevmonth' : prevmonth,
            'prevyear' : prevyear,
            'nextmonth' : nextmonth,
            'nextyear' : nextyear,
            'year' : year,
            'month': calendar.month_name[month],
            'gesamt' : gesamt,
        })
    else:
        print('NO HTMX REQUEST')
        

@login_required
def wall_of_fame(request):
    if request.htmx:
        year = 2024
        month = timezone.now().month
        mvplist = []
        locale.setlocale(locale.LC_ALL, 'de_DE')
        
        for i in range(month):
            m_name = calendar.month_name[i]
            deals_this_month = Deal.objects.filter(
            deal_closed_at__month=i).filter(deal_closed_at__year=year)
            #print(deals_this_month)
            if deals_this_month.count() == 0:
                continue
            userdictmonth = {}
            userdictmonth.clear()
            gesamt = 0
            
            for d in deals_this_month:
                gesamt += d.amount
                if not d.user in userdictmonth:
                    userdictmonth[d.user] = {'revenue': 0, 'deals': 0, 'user': d.user, 'month': m_name}
                rev = d.amount
                if d.shares():
                        for s in d.shares():
                            rev -= (d.amount * s.prozente/100)

                userdictmonth[d.user]['revenue'] += rev
                userdictmonth[d.user]['deals'] += 1
            for d in deals_this_month:
                rev = d.amount
                for share in d.shares():
                    if not share.user in userdictmonth:
                        userdictmonth[share.user] = {'revenue': 0, 'deals': 0, 'user': share.user, 'month': m_name}
                    userdictmonth[share.user]['revenue'] += (d.amount * share.prozente/100)
                    userdictmonth[share.user]['deals'] += 1

                
            

            userdictmonth = dict(
            sorted(userdictmonth.items(), key=lambda x: x[1]['revenue'], reverse=True))


            allkeys = list(userdictmonth.keys())
        
            try:
                mvplist.append(userdictmonth[allkeys[0]])
            except Exception as e:
                print(e)

        mvplist.reverse()
        locale.setlocale(locale.LC_ALL, 'de_DE')
        m_name = calendar.month_name[month],
        return render(request, 'billerboard/partials/wall_of_fame.html',{
            'mvplist': mvplist,

        })
    else:
        print('NO HTMX REQUEST')


@login_required()
def team(request):
    return render(request, 'billerboard/team.html')


@login_required()
def deals(request):
    # if superuser fetch all deals
    if request.user.is_superuser:
        deals = Deal.objects.all().order_by('-deal_closed_at')
    # else fetch only deals of the current user
    else:
        id_list = []
        deals_id = Deal.objects.filter(
            user=request.user).order_by('-deal_closed_at')
        for deal in deals_id:
            id_list.append(deal.id)
        shares = Share.objects.filter(user=request.user)
        for share in shares:
            id_list.append(share.deal.id)

        deals = Deal.objects.filter(id__in=id_list).order_by('-deal_closed_at')
    return render(request, 'billerboard/deals.html', {'deals': deals})
@login_required()
def deal_genehmigen(request, deal_id):
    if request.user.is_superuser:
        deal = Deal.objects.get(id=deal_id)
        deal.genehmigt = True
        deal.genehmigt_von = request.user
        deal.save()
        return redirect('deals')

@login_required()
def deal_storno(request, deal_id):
    if request.user.is_superuser:
        deal = Deal.objects.get(id=deal_id)
        deal.storniert = True
        deal.storniert_von = request.user
        deal.storniert_am = timezone.now()
        deal.save()
        return redirect('deals')


@login_required()
def deals_user(request, user_id):
    id_list = []
    deals_id = Deal.objects.filter(user=user_id).order_by('-deal_closed_at')
    for deal in deals_id:
        id_list.append(deal.id)
    shares = Share.objects.filter(user=user_id)
    for share in shares:
        id_list.append(share.deal.id)
    deals = Deal.objects.filter(id__in=id_list).order_by('-deal_closed_at')

    return render(request, 'billerboard/deals.html', {'deals': deals})


@login_required()
def deal_einreichen(request):
    if request.method == 'GET':
        dealform = DealForm()
        return render(request, 'billerboard/deal_einreichen.html', {'dealform': dealform})
    if request.method == 'POST':
        dealform = DealForm(request.POST)
        if dealform.is_valid():
            deal = dealform.save(commit=False)
            deal.user = request.user
            if deal.kandidat and deal.unternehmen:
                deal.save()
                return redirect('deal_daten_einreichen', deal_id=deal.id)
            else:
                messages.error(request, 'Bitte Kandidat und Unternehmen auswählen')
            
        return render(request, 'billerboard/deal_einreichen.html', {'dealform': dealform})


@login_required()
def deal_daten_einreichen(request, deal_id):
    deal = Deal.objects.get(id=deal_id)
    print(deal)
    if request.method == 'GET':
        dealdatenform = DealDatenUploadForm()
        return render(request, 'billerboard/daten_einreichen.html', {'dealdatenform': dealdatenform})
    
    if request.method == 'POST':
        dealdatenform = DealDatenUploadForm(request.POST, request.FILES)
        print(request.POST)
        print(request.FILES)
        if dealdatenform.is_valid():
            agb = DealDaten.objects.create(deal=deal, name='AGB', datei=dealdatenform.cleaned_data['agb'])
            vertrag = DealDaten.objects.create(deal=deal, name='Vertrag', datei=dealdatenform.cleaned_data['vertrag'])
            dsgvo = DealDaten.objects.create(deal=deal, name='DSGVO', datei=dealdatenform.cleaned_data['dsgvo'])
            serviceabrechnung = DealDaten.objects.create(deal=deal, name='Serviceabrechnung', datei=dealdatenform.cleaned_data['serviceabrechnung'])

            # Create Success Message
            messages.success(request, 'Daten erfolgreich eingereicht')

            
            # Send Email
            datenlink = f'https://stoneberg.work/deals/dealdaten/{deal.id}'
            subject = f'Neuer Deal von Stoneberg von {deal.user.first_name} {deal.user.last_name} eingereicht'
            html_message = render_to_string('email/neuer_deal_abrechnung.html', {'deal': deal,
                                                                                 'datenlink': datenlink,
                                                                                })
            plain_message = strip_tags(html_message)
            from_email = 'Stoneberg Billerboard <no-reply@stoneberg.work>'
            to = "thuy.dokim@stoneberg-it.de"
            mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
            to ="rick.stawitzki@stoneberg.de"
            mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
            return redirect('dashboard')
        else:
            print(dealdatenform.errors)
            return render(request, 'billerboard/daten_einreichen.html', {'dealdatenform': dealdatenform, 
                                                                         'error': dealdatenform.errors})


@login_required()
def datenzip(request, deal_id):
    if request.user.is_superuser:
        deal = Deal.objects.get(id=deal_id)
        dealdaten = DealDaten.objects.filter(deal=deal)
        files = []
        for d in dealdaten:
            files.append(d.datei)
        response = HttpResponse(content_type='application/zip')
        zip_file = f'{deal.unternehmen}_{deal.kandidat}_daten.zip'
        response['Content-Disposition'] = f'attachment; filename={zip_file}'
        with zipfile.ZipFile(response, 'w') as zipf:
            for f in files:
                zipf.write(f.path, f.name)
        return response
    else:
        return redirect('dashboard')

@login_required()
def einzahlung(request):
    # eine einzahlung vom kunden verbuchen
    einzahlungen = Einzahlung.objects.all().order_by('-einzahlung_added_at')
    if request.method == 'GET':
        einzahlungsform = EinzahlungsForm()

        return render(request, 'billerboard/einzahlung.html', {'einzahlungsform': einzahlungsform, 'einzahlungen': einzahlungen})
    if request.method == 'POST':
        einzahlungsform = EinzahlungsForm(request.POST)
        if einzahlungsform.is_valid():
            einzahlung = einzahlungsform.save(commit=False)
            einzahlung.eingetragen_von = request.user
            einzahlung.save()
            return render(request, 'billerboard/einzahlung.html', {'einzahlungsform': einzahlungsform, 'einzahlungen': einzahlungen})

@login_required()
def partnerliste(request):
    partner = PartnerUnternehmen.objects.all()
    partnerform = PartnerListenForm()
    if request.method == 'GET':
        return render(request, 'billerboard/partnerliste.html',{ 'partner': partner, 'partnerform': partnerform})
    if request.method == 'POST':
        partnerform = PartnerListenForm(request.POST)
        if partnerform.is_valid():
            p = partnerform.save(commit=False)
            p.partnerunternehmen_added_by = request.user
            p.partnerunternehmen_updated_by = request.user
            p.save()
            return render(request, 'billerboard/partnerliste.html',{ 'partner': partner, 'partnerform': partnerform})
        else:
            print(partnerform.errors)
    return render(request, 'billerboard/partnerliste.html',{ 'partner': partner, 'partnerform': partnerform})

@login_required()
def blackliste(request):
    blacklist = BlacklistUnternehmen.objects.all()
    blacklistform = BlackListenForm()
    if request.method == 'GET':
        return render(request, 'billerboard/blackliste.html',{ 'blacklist': blacklist, 'blacklistform': blacklistform})
    if request.method == 'POST':
        blacklistform = BlackListenForm(request.POST)
        if blacklistform.is_valid():
            b = blacklistform.save(commit=False)
            b.blacklist_added_by = request.user
            b.blacklist_updated_by = request.user
            b.save()
            return render(request, 'billerboard/blackliste.html',{ 'blacklist': blacklist, 'blacklistform': blacklistform})
        else:
            print(blacklistform.errors)
            return render(request, 'billerboard/blackliste.html',{ 'blacklist': blacklist, 'blacklistform': blacklistform})
@login_required()
def hotjobs(request):
    return render(request, 'billerboard/hotjobs.html')

@csrf_exempt
def createhubspotcandidate(request):

    if request.method == 'POST':
        print(request.POST)
        print(request.body)
        j = request.body.decode('utf-8')
        j = json.loads(j)
        print(j)
        if not Kontakt.objects.filter(kontakt_hubspotid=j['id']).exists():
            kontakt = Kontakt.objects.create(kontakt_hubspotid=j['id'], 
                                            anrede=j['salutation'],
                                            vorname=j['firstname'],
                                            nachname=j['lastname'],
                                            email=j['email'],
                                            telefon=j['phone'],
                                            position=j['jobtitle'],
                                            )
        kandidat = Kandidat.objects.create(kontakt=kontakt,
                                           berufsbezeichnung=j['jobtitle'])
        #print(request.POST['candidate_id'])
    
    return HttpResponse(status=200)
@login_required()
def sendhubspotcandidate(request):

    if request.method == 'GET':
        form = KandidatHubspotForm()
        return render(request, 'billerboard/sendhubspotcandidate.html', {'form': form})
    if request.method == 'POST':
        form = KandidatHubspotForm(request.POST)
        hid = form.data['candidate_id']
        url = 'https://hooks.zapier.com/hooks/catch/16629760/3qcwgvo/'
        headers = {
            'Content-Type': 'json',
            'pw': 'stoneberg',

        }
        payload = {
            'candidate_id': hid
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        print(response.text)
        print(response.status_code)
        return redirect('dashboard')


@csrf_exempt
def createhubspotunternehmen(request):
    if request.method == 'POST':
        print(request.POST)
        print(request.body)
        j = request.body.decode('utf-8')
        j = json.loads(j)
        print(j)
        if not Unternehmen.objects.filter(unternehmen_hubspotid=j['id']).exists():
            if not Unternehmen.objects.filter(name=j['name']).exists():
                Unternehmen.objects.create(unternehmen_hubspotid=j['id'],
                                                         name=j['name'],
                                                         plz=j['zip'],
                                                         strasse_hausnummer = j['address'],
                                                         ort=j['city'],
                                                         website=j['domain'],
                                                         )
                
                
                                                         

    return HttpResponse(status=200)
@login_required()
def sendhubspotunternehmen(request):

    if request.method == 'GET':
        form = UnternehmenHubspotForm()
        return render(request, 'billerboard/sendhubspotunternehmen.html', {'form': form})
    if request.method == 'POST':
        form = UnternehmenHubspotForm(request.POST)
        hid = form.data['unternehmen_id']
        url = 'https://hooks.zapier.com/hooks/catch/16629760/3qcx68k/'
        headers = {
            'Content-Type': 'json',
            'pw': 'stoneberg',

        }
        payload = {
            'unternehmen_id': hid
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        print(response.text)
        print(response.status_code)
        return redirect('dashboard')

@login_required()
def addivboard(request):
    if request.method == 'GET':
        form = InterviewBoardForm()
        return render(request, 'billerboard/add_ivboard.html',{ 'form': form})
    if request.method == 'POST':
        form = InterviewBoardForm(request.POST)
        if form.is_valid():
            iv = form.save()
            iv.owner = request.user
            iv.save()
            return redirect('dashboard')
        else:
            print(form.errors)
            return render(request, 'billerboard/add_ivboard.html',{ 'form': form})
@login_required()
def alleivboards(request):

    boards = InterviewBoard.objects.all()

    return render(request, 'billerboard/alle_ivboards.html', {'alleboards': boards})
@login_required()
def ivboard(request, ivboard_id):
    if request.method == 'GET':
        board = InterviewBoard.objects.get(id=ivboard_id)
        entries = InterviewBoardEntry.objects.filter(board=board).filter(ist_aktuell=True)   
        ivh = 0
        ivtw = 0
        ivnw = 0
        offer = 0
        revenue = 0
        for e in entries:
            ivh += e.iv_heute
            ivtw += e.iv_this_week
            ivnw += e.iv_next_week
            offer += e.offer
            revenue += e.revenue
        offers = Offer.objects.filter(board=board)
        return render(request, 'billerboard/ivboard.html', {'board': board, 
                                                            'entries': entries, 
                                                            'form': AddMemberToBoardForm(boardid=ivboard_id),
                                                            'offerform': OfferEntryForm(boardid=ivboard_id),
                                                            'offers': offers,
                                                            'ivh': ivh,
                                                            'ivtw': ivtw,
                                                            'ivnw': ivnw,
                                                            'offer': offer,
                                                            'revenue': revenue,
                                                            })
    if request.method == 'POST':
        form = AddMemberToBoardForm(request.POST, boardid=ivboard_id)
        if form.is_valid():
            user = form.cleaned_data['user']
            print(user)
            board = InterviewBoard.objects.get(id=ivboard_id)
            for u in user:
                if not InterviewBoardEntry.objects.filter(board=board, user=u).exists():
                    InterviewBoardEntry.objects.create(board=board, user=u)
            return redirect('ivboard', ivboard_id=ivboard_id)
        else:
            print(form.errors)
            return render(request, 'billerboard/ivboard.html', {'board': board, 'entries': entries, 'form': form})

def createoffer(request, board_id):
    if request.method == 'POST':
        form = OfferEntryForm(request.POST, boardid=board_id)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.board = InterviewBoard.objects.get(id=board_id)
            offer.save()
            return redirect('ivboard', ivboard_id=board_id)
        else:
            print(form.errors)
            return redirect('ivboard', ivboard_id=board_id)

@login_required()
def ivboardall(request):
    entries = InterviewBoardEntry.objects.filter(ist_aktuell=True)
    ivh = 0
    ivtw = 0
    ivnw = 0
    offer = 0
    revenue = 0
    for e in entries:
        ivh += e.iv_heute
        ivtw += e.iv_this_week
        ivnw += e.iv_next_week
        offer += e.offer
        revenue += e.revenue
    return render(request, 'billerboard/ivboardall.html', {'entries': entries,
                                                           'ivh': ivh,
                                                          'ivtw': ivtw,
                                                          'ivnw': ivnw,
                                                          'offer': offer,
                                                          'revenue': revenue,})

def updateivtoday(request, entry_pk):
    entry =  get_object_or_404(InterviewBoardEntry, pk=entry_pk)
    entry.iv_heute = request.POST['value']
    entry.save()
    message = "Save successful"
    return HttpResponse(message)

def updateivthisweek(request, entry_pk):
    entry =  get_object_or_404(InterviewBoardEntry, pk=entry_pk)
    entry.iv_this_week = request.POST['value']
    entry.save()
    message = "Save successful"
    return HttpResponse(message)

def updateivnextweek(request, entry_pk):
    entry =  get_object_or_404(InterviewBoardEntry, pk=entry_pk)
    entry.iv_next_week = request.POST['value']
    entry.save()
    message = "Save successful"
    return HttpResponse(message)

def updateoffer(request, entry_pk):
    entry =  get_object_or_404(InterviewBoardEntry, pk=entry_pk)
    entry.offer = request.POST['value']
    entry.save()
    message = "Save successful"
    return HttpResponse(message)

def updaterevenue(request, entry_pk):
    entry =  get_object_or_404(InterviewBoardEntry, pk=entry_pk)
    entry.revenue = request.POST['value']
    entry.save()
    message = "Save successful"
    return HttpResponse(message)

def prozessboard(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            prozesse = ProzessEntry.objects.filter(ist_abgeschlossen=False)
            offers = Offer.objects.filter(ist_abgeschlossen=False)
            return render(request, 'billerboard/prozessboard.html', {'prozesse': prozesse, 
                                                                        'offers': offers,
                                                                     'form': ProzessEntryForm(),
                                                                     'anzahl_prozesse': prozesse.count(),
                                                                     'gesamt_revenue': sum([p.revenue for p in prozesse]),})
        if request.method == 'POST':
            form = ProzessEntryForm(request.POST)
            if form.is_valid():
                f = form.save(commit=False)
                f.eingetragen_von = request.user
                f.save()
                return redirect('prozessboard')
            else:
                print(form.errors)
                return render(request, 'billerboard/prozessboard.html', {'form': form})
    else:
        return redirect('dashboard')
@login_required()
def prozess_schliessen_won(request, prozess_id):
    if request.user.is_superuser:
        prozess = ProzessEntry.objects.get(id=prozess_id)
        prozess.ist_abgeschlossen = True
        prozess.won = True
        prozess.abgeschlossen_am = timezone.now()
        prozess.save()
        return redirect('prozessboard')
    else:
        return redirect('dashboard')

@login_required()
def prozess_schliessen_lost(request, prozess_id):
    if request.user.is_superuser:
        prozess = ProzessEntry.objects.get(id=prozess_id)
        prozess.ist_abgeschlossen = True
        prozess.lost = True
        prozess.abgeschlossen_am = timezone.now()
        prozess.save()
        return redirect('prozessboard')
    else:
        return redirect('dashboard')


@login_required()
def offer_schliessen_lost(request, offer_id):
    if request.user.is_superuser:
        if request.htmx:
            if request.method == 'GET':
                print(offer_id)
                return render(request, 'billerboard/partials/offer_schliessen_modal.html', {'offer_id': offer_id})
        if request.method == 'POST':
            offer = Offer.objects.get(id=offer_id)
            offer.ist_abgeschlossen = True
            offer.lost = True
            offer.lost_reason = request.POST['reason']
            offer.abgeschlossen_am = timezone.now()
            offer.save()
            return redirect('prozessboard')

def offer_schliessen_won(request, offer_id):    
    if request.user.is_superuser:
        offer = Offer.objects.get(id=offer_id)
        offer.ist_abgeschlossen = True
        offer.won = True
        offer.abgeschlossen_am = timezone.now()
        offer.save()
        return redirect('prozessboard')
    else:
        return redirect('dashboard')
            

def prozessboard_alte_prozesse(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            prozesse = ProzessEntry.objects.filter(ist_abgeschlossen=True)
            offer = Offer.objects.filter(ist_abgeschlossen=True)
            return render(request, 'billerboard/prozess_static.html', {'prozesse': prozesse, 
                                                                     'form': ProzessEntryForm(),
                                                                     'anzahl_prozesse': prozesse.count()+offer.count(),
                                                                     'gesamt_revenue': sum([p.revenue for p in prozesse]),})

@login_required()
def toolrechnung(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            rechnungen = ToolKostenRechnung.objects.all()
            return render(request, 'billerboard/toolrechnung.html', {'form': AddUserToInvoice(),
                                                                     'rechnungen': rechnungen})
        if request.method == 'POST':
            tools = Tool.objects.all()
            gesamt = 0
            f = []
            for t in tools:
                f.append(t.toolname)
                gesamt += t.kosten
            f = ', '.join(f)
            form = AddUserToInvoice(request.POST)
            if form.is_valid():
                user = form.cleaned_data['user']
                print(user)
                for u in user:
                    print(user)
                    rechnungsdaten = RechnungsDaten.objects.get(user=u)
                    url = "https://api.lexoffice.io/v1/invoices"
                    print(timezone.now().isoformat('T', 'milliseconds'))
                    payload = json.dumps({
                        "id": None,
                        "organizationId": None,
                        "createdDate": None,
                        "updatedDate": None,
                        "version": None,
                        "archived": False,
                        "voucherStatus": None,
                        "voucherNumber": None,
                        "voucherDate": f"{timezone.now().isoformat('T', 'milliseconds')}", # "2024-03-06T00:00:00.000+02:00",
                        "dueDate": None,
                        "address": {
                            "contactId": None,
                            "name": rechnungsdaten.firmenname,
                            "street": rechnungsdaten.strasse,
                            "city": rechnungsdaten.ort,
                            "zip": rechnungsdaten.plz,
                            "countryCode": "DE"
                        },
                        "lineItems": [
                            {
                            "id": None,
                            "type": "custom",
                            "name": "Lizenznutzung",
                            "description": f"Tools: {f}",
                            "quantity": 3,
                            "unitName": "Monate",
                            "unitPrice": {
                                "currency": "EUR",
                                "netAmount": f'{gesamt}',
                                "taxRatePercentage": 19
                            },
                            },
                            {
                            "type": "text",
                            "name": "Strukturieren Sie Ihre Belege durch Text-Elemente.",
                            "description": "Das hilft beim Verständnis"
                            }
                        ],
                        "totalPrice": {
                            "currency": "EUR",
                        },
                        "taxConditions": {
                            "taxType": "net",
                            "taxTypeNote": None
                        },
                        "shippingConditions": {
                            "shippingDate": f"{timezone.now().isoformat('T', 'milliseconds')}", # "2024-03-06T00:00:00.000+02:00",
                            "shippingEndDate": None,
                            "shippingType": "delivery"
                        },
                        "title": "Rechnung",
                        "introduction": "Unsere Lieferungen/Leistungen stellen wir Ihnen wie folgt in Rechnung.",
                        "remark": """Diese Rechnung wurde im Factoringverfahren an die Wolf Factoring, Robert Wolf GmbH, Esslinger Str. 7, 70771 LE-Echterdingen, übertragen. Eine Zahlung kann somit nur an diese mit schuldbefreiender Wirkung erfolgen. Bitte bezahlen Sie an Kontoinhaber:
                        Robert Wolf GmbH, KSK Esslingen,
                        IBAN-Code: DE40 6115 0020 0100 666306; BIC-Code: ESSLDE66XXX

                        Vielen Dank für die gute Zusammenarbeit."""
                        })
                
                    headers = {
                    'Authorization': 'Bearer _hTkaSsxsM1-MgUhsq7bJU7wxPQ2JkyNxvJfwmcMJpBcq9iw',
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                    }
                    response = requests.request("POST", url, headers=headers, data=payload)
                    ToolKostenRechnung.objects.create(rechnung_fuer=u, lexoffice_id=response.json()['id'], gesamtsumme=gesamt)
                    print(response.json())
                return redirect('toolrechnung')
            else:
                print(form.errors)
                return render(request, 'billerboard/toolrechnung.html', {'form': form})
    else:
        return redirect('dashboard')
@login_required()
def rechnungsdaten(request):
    if request.method == 'GET':
        try:
            rechnungsdaten = get_object_or_404(RechnungsDaten, user=request.user)
            return render(request, 'billerboard/rechnungsdaten.html', {'form': RechnungsDatenForm(instance=rechnungsdaten)})
        except:
            return render(request, 'billerboard/rechnungsdaten.html', {'form': RechnungsDatenForm()})
    if request.method == 'POST':
        if RechnungsDaten.objects.filter(user=request.user).exists():
            form = RechnungsDatenForm(request.POST, instance=RechnungsDaten.objects.get(user=request.user))
        else:
            HttpResponse('Rechnungsdaten existieren nicht')
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()
            
            return redirect('dashboard')
        else:
            print(form.errors)
            return render(request, 'billerboard/rechnungsdaten.html', {'form': form})

@login_required()
def toolkostenrechnung_bezahlt(request, rechnung_id):
    if request.user.is_superuser:
        rechnung = ToolKostenRechnung.objects.get(id=rechnung_id)
        rechnung.bezahlt = True
        rechnung.bezahlt_am = timezone.now()
        rechnung.save()
        return redirect('toolrechnung')
    else:
        messages.warning(request, 'Keine Berechtigung!')
        return redirect('dashboard')

@login_required()
def rang_overview(request):
    if request.user.is_superuser:
        if request.htmx:
            if request.method == 'POST':
                user = User.objects.filter(
                    Q(first_name__icontains=request.POST['search']) | Q(last_name__icontains=request.POST['search']))
                profilelist = []
                for u in user:
                    profilelist.append(u.profile)
                ranks = RangHistory.objects.filter(user__in=profilelist)
                return render(request, 'billerboard/partials/rank_search.html', {'ranks': ranks})
        else:
            return render(request, 'billerboard/rang_overview.html')
        

# def daily_survey
@login_required()
def daily_survey(request):
    if request.method == 'GET':
        questions = DailySurveyQuestion.objects.all().order_by('?').values('id', 'data', 'level')
        list_user = User.objects.filter(profile__team_lead=request.user)
        print(list(list_user))
        return render(request, 'billerboard/daily_survey.html', {"questions": questions, "list_user": list_user})

    if request.method == 'POST':
        user = request.user
        body = json.loads(request.body) # Log body của request
        responses = []
        user_survey = User.objects.get(username=body['user_survey'])
        dailySurvey = DailySurvey.objects.create(user=user,user_survey=user_survey)
        
        for data in body['formData']:
            question = DailySurveyQuestion.objects.get(id=int(data['question_id']))
            responses.append(DailySurveyAnswer(
                    user=user,
                    question=question,
                    data=data['answer'],
                    dailySurvey=dailySurvey
                ))
        
        for data in body['formKandidates']:
            kontakt = Kontakt.objects.create(
                anrede = data['anrede'],
                position = data['position'],
                vorname = data['vorname'],
                email = data['email'],
                telefon = data['telefon'],
                nachname = data['nachname'],
                kontakt_hubspotid = data['kontakt_hubspotid'],
                doer = data['doer'],
                ist_ansprechpartner = data['ist_ansprechpartner'],
            )
            Kandidat.objects.create(kontakt = kontakt, berufsbezeichnung = data['berufsbezeichnung'])
        
        DailySurveyAnswer.objects.bulk_create(responses)
        messages.success(request, 'Survey submitted successfully!')
        return render(request, 'billerboard/daily_survey.html')


@login_required()
def getListSurvey(request):
    if(request.method == 'GET'):
        daily_surveys = DailySurvey.objects.filter(user=request.user).select_related('user').prefetch_related('dailysurveyanswer_set__question')
        print(list(daily_surveys))
        survey_data = []
        for survey in daily_surveys:
            answers = []
            for answer in survey.dailysurveyanswer_set.all():
                answers.append({
                    'answer': answer.data,
                    'question': answer.question.data,
                })
            survey_data.append({
                'role': survey,
                'answers': answers,
                'created_at': survey.created_at,
                
            })
        
        return render(request, 'billerboard/daily_survey_list.html', {"survey_data": survey_data})
           
         
def getListStaff(request):
    if(request.method == 'GET'):
        staffs = User.objects.select_related('profile__address__state')
    return render(request, 'billerboard/staff_list.html', {"staffs": staffs})

def getListStaffApi(request):
    staffs = User.objects.select_related('profile__address__state')
    
    staff_data = []
    for user in staffs:
        try:
            address = user.profile.address
            state_name = address.state.name
            state_code = address.state.code
            staff_data.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'state_name': state_name,
                'state_code': state_code,
            })
        except AttributeError:
            staff_data.append({
                'username': user.username,
                'email': user.email,
                'state_name': None,
                'state_code': None,
            })
    
    return JsonResponse(staff_data, safe=False)