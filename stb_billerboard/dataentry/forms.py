from django.forms import ModelForm
from django import forms
from .models import ListenImport, Entry, EntryRate, DataEntryProfile
from billerboard.models import Unternehmen, Kontakt
class ListenImportForm(ModelForm):
    class Meta:
        model = ListenImport
        fields = ['name', 'liste', 'fuer']
        widgets = {
            'liste' : forms.FileInput(attrs={'accept': '.xlsx, .xls, .csv'}),
        }

class DataEntryKontaktForm(ModelForm):
    class Meta:
        model = Kontakt
        fields = ['anrede','vorname', 'nachname', 'email', 'telefon', 'position', 'ist_ansprechpartner' ]
        widgets = {
            'anrede': forms.Select(attrs={'class': 'form-control'}),
            'vorname': forms.TextInput(attrs={'class': 'form-control'}),
            'nachname': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'telefon': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
           
        }
        labels = {
            'anrede': 'Anrede*',
            'vorname': 'Vorname',
            'nachname': 'Nachname*',
            'email': 'E-Mail*',
            'telefon': 'Telefon',
            'position': 'Position*',
            'ist_ansprechpartner': 'Ist Ansprechpartner',
        }

class DataEntryUnternehmenForm(ModelForm):
    class Meta:
        model = Unternehmen
        fields = ['name', 'website', 'plz', 'strasse_hausnummer', 'ort', 'telefon']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.TextInput(attrs={'class': 'form-control'}),
            'plz': forms.TextInput(attrs={'class': 'form-control'}),
            'strasse_hausnummer': forms.TextInput(attrs={'class': 'form-control'}),
            'ort': forms.TextInput(attrs={'class': 'form-control'}),
            'telefon': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Name*',
            'website': 'Website',
            'plz': 'PLZ',
            'strasse_hausnummer': 'Straße und Hausnummer',
            'ort': 'Ort',
            'telefon': 'Telefon',
        }