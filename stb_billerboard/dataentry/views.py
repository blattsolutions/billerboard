from django.shortcuts import render,redirect, get_object_or_404
from .models import ListenImport, Entry, EntryRate, Liste, ListAssignment, DataEntryProfile
from billerboard.models import Unternehmen, Kontakt
from django.utils import timezone
import datetime
from faker import Faker
from .forms import ListenImportForm, DataEntryKontaktForm, DataEntryUnternehmenForm
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.
from .tasks import gehschlafen, handlelist

from functools import wraps
import time

def timer(func):
    """helper function to estimate view execution time"""

    @wraps(func)  # used for copying func metadata
    def wrapper(*args, **kwargs):
        # record start time
        start = time.time()

        # func execution
        result = func(*args, **kwargs)
        
        duration = (time.time() - start) * 1000
        # output execution time to console
        print('view {} takes {:.2f} ms'.format(
            func.__name__, 
            duration
            ))
        return result
    return wrapper

@timer
def dashboard(request):
    zahl_unternehmen = Unternehmen.objects.count()
    zahl_kontakte = Kontakt.objects.count()
    kontakte_added_this_month = Kontakt.objects.filter(kontakt_added_at__month=timezone.now().month).count()
    unternehmen_added_this_month = Unternehmen.objects.filter(unternehmen_added_at__month=timezone.now().month).count()
    unternehmen_last_month = Unternehmen.objects.filter(unternehmen_added_at__month=timezone.now().month-1).count()
    kontakte_last_month = Kontakt.objects.filter(kontakt_added_at__month=timezone.now().month-1).count()
    difference_unternehmen = unternehmen_added_this_month - unternehmen_last_month
    difference_kontakte = kontakte_added_this_month - kontakte_last_month
    letzter_import = ListenImport.objects.last()
    importe = Liste.objects.all()
    fimport = ListenImport.objects.filter(erfolgreich=False)
    kosten_dieser_monat = 0
    for entry in Entry.objects.filter(time_started__month=timezone.now().month).select_related('rate'):
        try:
            kosten_dieser_monat += entry.rate.rate
        except:
            pass
    kosten_letzter_monat = 0
    for entry in Entry.objects.filter(time_started__month=timezone.now().month-1).select_related('rate'):
        try:
            kosten_letzter_monat += entry.rate.rate
        except:
            pass
    difference_kosten = kosten_dieser_monat - kosten_letzter_monat
    letzte_zehn_imports = Liste.objects.all()[:10]
    listen = Liste.objects.all()

    userdict = {}
    for e in Entry.objects.filter(time_finished__month=timezone.now().month).select_related('rate', 'assigned_to'):
        if not e.assigned_to in userdict:
            userdict[e.assigned_to] = {'revenue' : e.rate.rate, 'deals' : 1}
        else:
            userdict[e.assigned_to]['revenue'] += e.rate.rate
            userdict[e.assigned_to]['deals'] += 1
    top3_performers = list(userdict.items())[:3]
    rest_performers = dict(list(userdict.items())[3:])
    print(userdict)
    print(top3_performers)

    return render(request, 'dataentry/dashboard.html', {'zahl_unternehmen': zahl_unternehmen, 
                                                       'zahl_kontakte': zahl_kontakte,
                                                       'kontakte_added_this_month': kontakte_added_this_month,
                                                       'unternehmen_added_this_month': unternehmen_added_this_month,
                                                       'failed_imports': fimport.count(),
                                                       'letzter_import': letzter_import,
                                                       'importe': importe,
                                                       'difference_unternehmen': difference_unternehmen,
                                                       'difference_kontakte': difference_kontakte,
                                                       'kosten_dieser_monat': kosten_dieser_monat,
                                                       'difference_kosten': difference_kosten,
                                                       'letzte_zehn_imports': letzte_zehn_imports,
                                                       'top3_performers' : top3_performers,
                                                        'rest_performers' : rest_performers,
                                                       'dataentry': True,})

def importlist(request):
    form = ListenImportForm()
    if request.method == 'GET':
        return render(request, 'dataentry/importlist.html', {'form': form})
    
    if request.method == 'POST':
        form = ListenImportForm(request.POST, request.FILES)
        print(request.POST)
        print(request.FILES)
        if form.is_valid():
            l = form.save()
            l.hochgeladen_von = request.user
            l.save()
            handlelist.delay(l.id)
            return redirect('dataentrydashboard')
        else:
            print(form.errors)
            return render(request, 'dataentry/importlist.html', {'form': form,
                                                                    'error': form.errors})

def new_data_entry_user(request):
    if request.method == 'GET':
        rates = EntryRate.objects.all()
        return render(request, 'dataentry/new_data_entry_user.html', {'rates': rates})
    if request.method == 'POST':
        print(request.POST)
        try:
            user = User.objects.create_user(request.POST['username'], 
                                            request.POST['email'], 
                                            request.POST['password'])
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.save()
            print('User Saved')
            profile = DataEntryProfile.objects.create(user=user, 
                                                      rate=EntryRate.objects.get(id=request.POST['rate']))
            profile.save()
            print('profile saved')
            return redirect('dataentrydashboard')
        except Exception as e:
            print(e)
            return render(request, 'dataentry/new_data_entry_user.html', {'error': 'Fehler beim Anlegen des Users'})

def entry(request, entry=None):
    #Priorities:
    #1. Entry with id
    #2. Last non finished entry (page refresh)
    #3. Skipped entry of other users
    #4. New Entry
    #5. Last entry on hold
    #6. Hold of other users


    if request.method == 'GET':
        if not request.user.dataentryprofile:
            return redirect('dashboard')
        #1 Getting Entry by id parameter
        if entry:
            entry = Entry.objects.get(id=entry)
            if entry.assigned_to != request.user:
                if not request.user.is_superuser:
                    return redirect('dataentrydashboard')
            if not entry.time_started:
                entry.time_started = timezone.now()
                entry.save()
            return render(request, 'dataentry/entry.html', {'assignment': entry, 
                                                            'unternehmenform': DataEntryUnternehmenForm(prefix='unternehmen', instance=entry.unternehmen), 
                                                            'kontaktform': DataEntryKontaktForm(prefix='kontakt')})
        
        #2 Getting last non finished entry
        if Entry.objects.filter(assigned_to=request.user).filter(time_finished__isnull=True).exclude(on_hold__isnull=False).exists():
            entry = Entry.objects.filter(assigned_to=request.user).filter(time_finished__isnull=True).exclude(on_hold__isnull=False).last()
            return render(request, 'dataentry/entry.html', {'assignment': entry, 
                                                            'unternehmenform': DataEntryUnternehmenForm(prefix='unternehmen', instance=entry.unternehmen), 
                                                            'kontaktform': DataEntryKontaktForm(prefix='kontakt')})
        
        #3 Getting skipped entry of other users
        if Entry.objects.filter(skipped__isnull=False).exists():
            entry = Entry.objects.filter(assigned_to=request.user).filter(skipped__isnull=False).filter(time_finished__isnull=False).last()
            if entry.assigned_to != request.user:
                entry.assigned_to = request.user
                entry.time_started = timezone.now()
                entry.save()
                return render(request, 'dataentry/entry.html', {'assignment': entry, 
                                                            'unternehmenform': DataEntryUnternehmenForm(prefix='unternehmen', instance=entry.unternehmen), 
                                                            'kontaktform': DataEntryKontaktForm(prefix='kontakt')})
            
        #4 Creating new Assignment if available
        if ListAssignment.objects.filter(kontakt__isnull=True).exists():
            empty_assignments = ListAssignment.objects.filter(kontakt__isnull=True)
            for assignment in empty_assignments:
                if not Entry.objects.filter(listassignment=assignment).exists():
                    entry = Entry.objects.create(assigned_to=request.user, listassignment=assignment)
                    entry.unternehmen = assignment.unternehmen
                    entry.time_started = timezone.now()
                    entry.save()
                    return render(request, 'dataentry/entry.html', {'assignment': entry, 
                                                                'unternehmenform': DataEntryUnternehmenForm(prefix='unternehmen', instance=entry.unternehmen), 
                                                                'kontaktform': DataEntryKontaktForm(prefix='kontakt')})    

        #5 Getting hold of other users
        if Entry.objects.filter(on_hold__isnull=False).exists():
            entry = Entry.objects.filter(on_hold__isnull=False).last()
            if entry.assigned_to != request.user:
                entry.assigned_to = request.user
                entry.time_started = timezone.now()
                entry.save()
                return render(request, 'dataentry/entry.html', {'assignment': entry, 
                                                            'unternehmenform': DataEntryUnternehmenForm(prefix='unternehmen', instance=entry.unternehmen), 
                                                            'kontaktform': DataEntryKontaktForm(prefix='kontakt')})

        #6 Getting last entry on hold
        if Entry.objects.filter(assigned_to=request.user).filter(on_hold__isnull=False).exists():
            entry = Entry.objects.filter(assigned_to=request.user).filter(on_hold__isnull=False).last()
            return render(request, 'dataentry/entry.html', {'assignment': entry, 
                                                            'unternehmenform': DataEntryUnternehmenForm(prefix='unternehmen', instance=entry.unternehmen), 
                                                            'kontaktform': DataEntryKontaktForm(prefix='kontakt')})
        
        
        #7 No entry available  
        messages.add_message(request, messages.SUCCESS, 'Keine Einträge mehr verfügbar')
        return redirect('dataentrydashboard')
        
        
        
    if request.method == 'POST':
        print(request.POST)
        if entry:
            entry = Entry.objects.get(id=entry)
            print('get entry from id')
        elif get_object_or_404(Entry, assigned_to=request.user, id=request.POST['assignment']):
            print('get entry from form')
            entry = get_object_or_404(Entry, assigned_to=request.user, id=request.POST['assignment'])
        print(entry.unternehmen.id)
        uinstance = Unternehmen.objects.get(id=entry.unternehmen.id)
        print(f'instance={uinstance.id}')
        unternehmenform = DataEntryUnternehmenForm(request.POST, instance=uinstance, prefix='unternehmen', )
        print(unternehmenform.instance.id)
        print(f'unternehmenform={unternehmenform}')
        kontaktform = DataEntryKontaktForm(request.POST, prefix='kontakt')
        print(unternehmenform.is_valid())
        print(unternehmenform.errors)
        print(f'Kontaktform valid: {kontaktform.is_valid()}')
        if unternehmenform.is_valid() and kontaktform.is_valid():
            print('both valid')
            unternehmen = unternehmenform.save()
            kontakt = kontaktform.save()
            print(kontakt)
            kontakt.eingetragen_von = request.user
            kontakt.save()
            print('kontakt gespeichert')
            print(kontakt)
            unternehmen.kontakte.add(kontakt)
            entry.unternehmen = unternehmen
            print(kontakt)
            entry.kontakt = kontakt
            entry.time_finished = timezone.now()
            entry.rate = request.user.dataentryprofile.rate
            entry.skipped = None
            entry.on_hold = None
            entry.save()
            if entry.listassignment:
                print('saving listassignment')
                assignment = entry.listassignment
                assignment.kontakt = kontakt
                assignment.unternehmen = unternehmen
                assignment.save()
            print('Saving profile')
            profile = request.user.dataentryprofile
            profile.lifetime_completed += 1
            profile.current_working = None
            profile.save()
            return redirect('entry')
        else:
            return render(request, 'dataentry/entry.html', {'assignment': entry, 
                                                        'unternehmenform': unternehmenform, 
                                                        'kontaktform': kontaktform})


def hold(request, entry):
    if request.method == 'GET':
        if request.user.dataentryprofile.on_hold_count < 10:
            entry = Entry.objects.get(id=entry)
            entry.hold
        return redirect('entry')


def refresh_liste(request, liste):
    if request.method == 'GET':
        handlelist.delay(liste)
        return redirect('dataentrydashboard')

def deuseroverview(request):
    if request.method == 'GET':
        users = DataEntryProfile.objects.all()
        return render(request, 'dataentry/deuseroverview.html', {'users': users})
@timer
def viewlist(request, listid):
    if request.method == 'GET':
        liste = Liste.objects.get(id=listid)
        assignments = ListAssignment.objects.filter(liste=liste).select_related('unternehmen', 'kontakt')
        print(assignments)
        return render(request, 'dataentry/viewlist.html', {'liste': liste, 'assignments': assignments})