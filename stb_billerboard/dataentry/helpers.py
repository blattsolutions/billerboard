from .models import ListenImport
from billerboard.models import Unternehmen, Kontakt
import pandas as pd
import numpy as np
from django.db import IntegrityError
import os
from pathlib import Path
from django.core.files import File


def listen_import(liste_id):
    print('test')
    try:
        dbliste = ListenImport.objects.get(id=liste_id)
        print(f'Importing Liste {dbliste}')
        liste = pd.read_excel(dbliste.liste)
        ap = None
        aplist = ['Ansprechpartner (Staff)', 
                  'Ansprechpartner Staff', 
                  'Staff', 
                  'Jobbezeichnung', 
                  'Ansprechpartner',
                  'Title', 
                  'Ansprechpartner (Staff) ', 
                  'Ansprechpartner Staff ', 
                  'Staff ', 
                  'Jobbezeichnung ', 
                  'Ansprechpartner ',
                  'Title ',
                  'Jobbezeichnung (Staff)']
        for i in aplist:
            if set([i]).issubset(liste.columns):
                ap = i
                break
        if ap is None:
            print('Falsche Spalten in Liste -> Quitting')
            dbliste.erfolgreich = False
            dbliste.grund = 'Falsche Spalten in Liste (Ansprechpartner)'
            dbliste.save()
            return
        emailliste = ['Email', 'E-Mail', 'E-Mail-Adresse', 'email']
        email = None
        for i in emailliste:
            if set([i]).issubset(liste.columns):
                email = i
                break
        if email is None:
            print('Falsche Spalten in Liste (Email) -> Quitting')
            dbliste.erfolgreich = False
            dbliste.grund('Falsche Spalten in Liste (Email)')
            dbliste.save()
            return
        tellist = ['Telefon', 'Telefonnummer', 'Telefonnummer (Staff)', 'Telefon (Staff)', 'Telephonnummer', 'Telephone', 'Telefonnummer ', 'Telefon ', 'Telefonnummer (Staff) ', 'Telefon (Staff) ', 'Telephonnummer ', 'Telephone']
        tel = None
        for i in tellist:
            if set([i]).issubset(liste.columns):
                tel = i
                break
        if tel is None:
            print('Falsche Spalten in Liste (Telefon) -> Quitting')
            dbliste.erfolgreich = False
            dbliste.grund = 'Falsche Spalten in Liste (Telefon)'
            dbliste.save()
            return
        companylist = ['Unternehmen', 'Firma', 'Firmenname', 'Firmenname (Staff)', 'Firmenname (Staff) ', 'Firmenname ', 'Firmenname (Staff)', 'company',]
        company = None
        for i in companylist:
            if set([i]).issubset(liste.columns):
                company = i
                break
        if company is None:
            print('Falsche Spalten in Liste (Unternehmen) -> Quitting')
            dbliste.erfolgreich = False
            dbliste.grund = 'Falsche Spalten in Liste (Unternehmen)'
            dbliste.save()
            return
        ortlist = ['Ort', 'Stadt', 'city', 'place']
        ort = None
        for i in ortlist:
            if set([i]).issubset(liste.columns):
                ort = i
                break
        if ort is None:
            print('Falsche Spalten in Liste (Ort) -> Quitting')
            dbliste.erfolgreich = False
            dbliste.grund = 'Falsche Spalten in Liste (Ort)'
            dbliste.save()
            return
        plzlist = ['PLZ', 'Postleitzahl', 'Postleitzahl (Staff)', 'Postleitzahl (Staff) ', 'Postleitzahl ', 'Postleitzahl (Staff)']
        plz = None
        for i in plzlist:
            if set([i]).issubset(liste.columns):
                plz = i
                break


    
        if not set([company, ort, 'Vorname', 'Nachname', ap, 'Anrede', email]).issubset(liste.columns):
            print('Falsche Spalten in Liste -> Quitting')
            dbliste.erfolgreich = False
            dbliste.grund = 'Falsche Spalten in Liste (spalten fehlen)'
            dbliste.save()
            return
        neue_unternehmen = 0
        neue_kontakte = 0
        for i, name in liste.iterrows():
            
            #Füge Unternehmen hinzu wenn es noch nicht existiert
            unternehmen_db = None
            try:
                adresselist = ['Straße und Hausnummer', 'Adresse', 'Adresse (Staff)', 'Adresse (Staff) ', 'Adresse ', 'Adresse (Staff)']
                adresse = None
                for i in adresselist:
                    if set([i]).issubset(liste.columns):
                        adresse = i
                        break
                websitelist = ['Website', 'Webseite', 'Website (Staff)', 'Website (Staff) ', 'Website ', 'Website (Staff)', 'Internet']
                website = None
                for i in websitelist:
                    if set([i]).issubset(liste.columns):
                        website = i
                        break
                unternehmen_db = Unternehmen.objects.create(name=name[company], ort=name[ort], telefon=name[tel])
                try:
                    if adresse:
                        unternehmen_db.strasse = name['adresse']
                except:
                    print('No Adresse')
                try:
                    if website:
                        unternehmen_db.webseite = name[website]
                except:
                    print('No Website')
                try:
                    if plz:
                        unternehmen_db.plz = name[plz]
                except:
                    print('No PLZ')
                unternehmen_db.save()
                neue_unternehmen += 1
            except IntegrityError as e:
                print(e)
        


            #Füge Kontakt hinzu wenn er noch nicht existiert
            try:
                u = Unternehmen.objects.get(name=name[company])
            except Unternehmen.DoesNotExist:
                print('Unternehmen existiert nicht')
                continue
            try:
                
                kontakt_db = Kontakt.objects.create(unternehmen=u, 
                                                    vorname=name['Vorname'], 
                                                    nachname=name['Nachname'], 
                                                    position=name[ap], 
                                                    anrede=name['Anrede'], 
                                                    email=name[email])
                neue_kontakte += 1
            except IntegrityError as e:
                print(e)
                continue
            
            try:
                kontakt_db.doer = name['Doer']
                kontakt_db.save()
            except:
                print('No doer')
            if kontakt_db.unternehmen == None:
                kontakt_db.delete()
                print('deleted')
                continue
            if kontakt_db.vorname == 'nan':
                kontakt_db.vorname = ''
                
            if kontakt_db.nachname == 'nan':
                kontakt_db.delete()
                print('deleted')
                continue
            if kontakt_db.position == 'nan':
                kontakt_db.position = ''
            if kontakt_db.anrede == 'nan':
                kontakt_db.delete()
                print('deleted')
                continue
            #yield "<br>Importiere Kontakt: " + str(kontakt_db)
        dbliste.erfolgreich = True
        dbliste.neue_unternehmen = neue_unternehmen
        dbliste.neue_kontakte = neue_kontakte
        dbliste.save()
    except Exception as E:
        dbliste.erfolgreich = False
        dbliste.grund = f'Hardfail in listen_import id: {liste_id}: {str(E)}'
        dbliste.save()
        print(f'Hardfail in listen_import id: {liste_id}: {str(E)}')


def import_alle_listen():
    for root, dirs, files in os.walk('media/alle_listen'):
        for file in files:
            if(file.endswith(".xlsx")):
                print(file)
                filepath = os.path.join(root, file)
                print(filepath)
                dbliste = ListenImport.objects.create(liste=file)
                f = open(filepath, 'rb')
                dbliste.liste = File(f, name=file)
                dbliste.save()
                f.close()
                listen_import(dbliste.id)
            

        




