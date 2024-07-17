from celery import shared_task
from time import sleep
from .models import ListenImport, Entry, EntryRate, Liste, ListAssignment, DataEntryProfile
from billerboard.models import Unternehmen, Kontakt
import pandas as pd
import numpy as np
from django.utils import timezone
from datetime import timedelta


@shared_task
def gehschlafen(printme):
    printme = printme
    print(f"Geschlafen: {printme}")
    sleep(10)
    print(f"Bin fertig: {printme}")

@shared_task
def handlelist(listimportid):
    print(f'Starte Import: {listimportid}')
    ulist = []
    neue_unternehmen = 0
    neue_kontakte = 0
    try:
        dbliste = ListenImport.objects.get(id=listimportid)
        print(f'Importing Liste {dbliste}')
        liste = pd.read_excel(dbliste.liste)
        liste.replace(np.nan, None, inplace=True)

        for i in liste.index:
            print(liste['Unternehmen'][i])
            if not Unternehmen.objects.filter(name=liste['Unternehmen'][i]).exists():
                u = Unternehmen.objects.create(name=liste['Unternehmen'][i])
                try:
                    website = liste['Internet'][i]
                    u.website = website
                except:
                    pass
                try:
                    email = liste['E-Mail'][i]
                    u.email = email
                except:
                    pass
                try:
                    telefon = liste['Telefon'][i]
                    u.telefon = telefon
                except:
                    pass
                try:
                    plz = liste['PLZ'][i]
                    u.plz = plz
                except:
                    pass
                try:
                    ort = liste['Ort'][i]
                    u.ort = ort
                except:
                    pass
                try:
                    strasse = liste['Straße und Hausnummer'][i]
                    strasse_hausnummer = strasse
                except:
                    pass

                u.save()
                ulist.append(u)
                neue_unternehmen += 1


            else:
                u = Unternehmen.objects.get(name=liste['Unternehmen'][i])
                ulist.append(u)
                #u.delete()
        
        #Füge Kontakt hinzu wenn er noch nicht existiert
        
            try:
                try:
                    apvorname = liste['Vorname - AP Anzeige'][i]
                except:
                    apvorname = None
                try:
                    apnachname = liste['Nachname - AP Anzeige'][i]
                except:
                    apnachname = None
                try:
                    apanrede = liste['Anrede - AP Anzeige'][i]
                except:
                    apanrede = None
                try:
                    apemail = liste['E-Mail - AP Anzeige'][i]
                except:
                    apemail = None
                if apvorname == 'nan':
                    apvorname = None
                if apnachname == 'nan':
                    apnachname = None
                if apanrede == 'nan':
                    apanrede = None
                if apemail == 'nan':
                    apemail = None

                if apanrede and apnachname and apemail:
                    if Kontakt.objects.filter(vorname=apvorname, nachname=apnachname, email=apemail).exists():
                        k = Kontakt.objects.get(vorname=apvorname, nachname=apnachname, email=apemail)
                        k.ist_ansprechpartner = True
                        k.save()
                        u.kontakte.add(k)
                        print('Ansprechpartner gefunden und gespeichert')
                    else:
                        if apanrede == 'Herr':
                            apanrede = 'Herr'
                        if apanrede == 'Frau':
                            apanrede = 'Frau'
                        k = Kontakt.objects.create(vorname=apvorname, nachname=apnachname, anrede=apanrede, email=apemail, ist_ansprechpartner=True)
                        k.save()
                        print('Neuer Kontakt angelegt')
                        neue_kontakte += 1
                    print(k)
                    u.kontakte.add(k)
                    u.save()
            except Exception as e:
                print(e)
        dbliste.erfolgreich = True


        try:
            liste = Liste.objects.create(import_liste=dbliste)
        except:
            liste = Liste.objects.get(import_liste=dbliste)
        for unternehmen in ulist:
            print(unternehmen)
            if ListAssignment.objects.filter(liste=liste, unternehmen=unternehmen).exists():
                print('ListAssignment existiert')
                assignment = ListAssignment.objects.get(liste=liste, unternehmen=unternehmen)
                assignment.offene_stellen +=1
                assignment.save()
                
            else:
                print('ListAssignment wird erstellt')
                assignment = ListAssignment.objects.create(liste=liste, unternehmen=unternehmen)
            try:
                assignment.liste = liste
                kontakte = unternehmen.kontakte.all()
                print(kontakte)
                for kontakt in kontakte:
                    if kontakt.ist_ansprechpartner:
                        assignment.kontakt = kontakt
                        
                        print('Kontakt zugeordnet')
                        break
                assignment.save()
            except Exception as e:
                print(e)

            
            
    except TypeError as e:
        print('Typeerror')


    except Exception as e:
        print(e)
        print('fail')
        dbliste.erfolgreich = False
        dbliste.grund = f'Hardfail in listen_import id: {dbliste.id}: {str(e)}'
        dbliste.save()


#Clean up Entries on hold
@shared_task
def clean_up_on_hold():
    print('Cleaning up on hold')
    for entry in Entry.objects.filter(on_hold__lte=timezone.now()-timedelta(minutes=30)):
        entry.on_hold = None
        entry.save()
        print(f'Entry {entry} cleaned up')


#Reset skips
@shared_task
def reset_skips():
    print('Resetting skips')
    for user in DataEntryProfile.objects.all():
        user.available_skips = 10
        user.save()
        print(f'Reset skips for {user}')