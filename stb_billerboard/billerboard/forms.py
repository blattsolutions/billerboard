from django.forms import ModelForm
from django import forms
from .models import Deal, DealDaten, Einzahlung, PartnerUnternehmen, ProzessEntry, Offer, ToolKostenRechnung, Unternehmen, BlacklistUnternehmen, InterviewBoard, InterviewBoardEntry
from userauth.models import RechnungsDaten
from django.contrib.auth.models import User



class UserChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        if obj.last_name or obj.first_name:
            display = " ".join((obj.first_name, obj.last_name))
        else:
            display = obj.username
        return display

class UserChoiceFieldSingle(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        if obj.last_name or obj.first_name:
            display = " ".join((obj.first_name, obj.last_name))
        else:
            display = obj.username
        return display


class DealForm(ModelForm):
    class Meta:
        model = Deal
        fields = ['deal_closed_at', 
                  'kandidat', 
                  'unternehmen', 
                  'antrittsdatum', 
                  'kulanz_bis', 
                  'amount',
                  'kandidat_von',
                  'unternehmen_von',
                  'abteilung']
        widgets = {
            'deal_closed_at': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'antrittsdatum': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'kulanz_bis': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'kandidat': forms.Select(attrs={'class': 'form-control selectpicker', 'data-live-search': 'true'}),
            'unternehmen': forms.Select(attrs={'class': 'form-control selectpicker', 'data-live-search': 'true'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'deal_closed_at': 'Deal geclosed am',
            'kandidat': 'Kandidat',
            'unternehmen': 'Unternehmen',
            'antrittsdatum': 'Antrittsdatum',
            'kulanz_bis': 'Kulanz bis (nur ausfüllen wenn eine Kulanz vereinbart wurde)',
            'amount': 'Dealsumme in €',
        }

class DealDatenForm(ModelForm):
    class Meta:
        model = DealDaten
        fields = ['name', 'datei']
        widgets = {
            'name': forms.Select(attrs={'class': 'form-control selectpicker'}),
            'datei': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Dokumentenname',
            'datei': 'Datei',
        }


class EinzahlungsForm(ModelForm):
    class Meta:
        model = Einzahlung
        fields = ['deal', 'amount', 'rechnungsnummer', ]
        widgets = {
            'deal': forms.Select(attrs={'class': 'form-control selectpicker', 'data-live-search': 'true'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'rechnungsnummer': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'deal': 'Deal auswählen',
            'amount': 'Einzahlungsbetrag in €',
            'rechnungsnummer': 'Rechnungsnummer',
        }

class PartnerListenForm(ModelForm):
    class Meta:
        model = PartnerUnternehmen
        fields = ['unternehmen', 'konditionen']
        widgets = {
            'unternehmen': forms.Select(attrs={'class': 'form-control selectpicker', 'data-live-search': 'true'}),
            'konditionen': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'unternehmen': 'Unternehmen',
            'konditionen': 'Konditionen',
        }

    def __init__(self, *args, **kwargs):
        super(PartnerListenForm, self).__init__(*args, **kwargs)

       
        # Erstellen einer Liste von IDs der Unternehmen, die bereits in PartnerUnternehmen vorhanden sind
        excludelistpartner = PartnerUnternehmen.objects.values_list('unternehmen__id', flat=True)
        excludelistblack = BlacklistUnternehmen.objects.values_list('unternehmen__id', flat=True)

        # Aktualisieren des QuerySets für das Feld 'unternehmen', um diese Unternehmen auszuschließen
        self.fields['unternehmen'].queryset = Unternehmen.objects.exclude(id__in=excludelistpartner).exclude(id__in=excludelistblack)

            

class BlackListenForm(ModelForm):
    class Meta:
        model = BlacklistUnternehmen
        fields = ['unternehmen', 'grund']
        widgets = {
            'unternehmen': forms.Select(attrs={'class': 'form-control selectpicker', 'data-live-search': 'true'}),
            'grund': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'unternehmen': 'Unternehmen',
            'grund': 'Grund für Blacklist',
        }

    def __init__(self, *args, **kwargs):
        super(BlackListenForm, self).__init__(*args, **kwargs)

        # Erstellen einer Liste von IDs der Unternehmen, die bereits in PartnerUnternehmen vorhanden sind
        excludelistpartner = PartnerUnternehmen.objects.values_list('unternehmen__id', flat=True)
        excludelistblack = BlacklistUnternehmen.objects.values_list('unternehmen__id', flat=True)

        # Aktualisieren des QuerySets für das Feld 'unternehmen', um diese Unternehmen auszuschließen
        self.fields['unternehmen'].queryset = Unternehmen.objects.exclude(id__in=excludelistpartner).exclude(id__in=excludelistblack)


class KandidatHubspotForm(forms.Form):
    candidate_id = forms.CharField(label='Kandidat ID', max_length=100)

    class Meta:
        fields = ['candidate_id']
        widgets = {
            'candidate_id': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'candidate_id': 'Kandidat ID in Hubspot',
        }

class UnternehmenHubspotForm(forms.Form):
    unternehmen_id = forms.CharField(label='Unternehmen ID', max_length=100)
    class Meta:
        fields = ['unternehmen_id']
        widgets = {
            'unternehmen_id': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'unternehmen_id': 'Unternehmen ID in Hubspot',
        }

class DealDatenUploadForm(forms.Form):
    agb = forms.FileField(label='AGB vom Kunden')
    dsgvo = forms.FileField(label='DSGVO vom Kandidaten')
    vertrag = forms.FileField(label='Vertrag')
    serviceabrechnung = forms.FileField(label='Serviceabrechnung')
    class Meta:
        fields = ['agb', 'dsgvo', 'vertrag', 'serviceabrechnung']
        widgets = {
            'agb': forms.FileInput(attrs={'class': 'form-control'}),
            'dsgvo': forms.FileInput(attrs={'class': 'form-control'}),
            'vertrag': forms.FileInput(attrs={'class': 'form-control'}),
            'serviceabrechnung': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'agb': 'AGB vom Kunden',
            'dsgvo': 'DSGVO vom Kunden',
            'vertrag': 'Vertrag',
            'serviceabrechnung': 'Serviceabrechnung',
        }


class InterviewBoardForm(ModelForm):
    class Meta:
        model = InterviewBoard
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AddMemberToBoardForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.boardid = kwargs.pop('boardid')
        super(AddMemberToBoardForm, self).__init__(*args, **kwargs)
        board = InterviewBoard.objects.get(id=self.boardid)
        useronboard = InterviewBoardEntry.objects.filter(board=board).values_list('user__id', flat=True)
        #get unique users on board only
        self.fields['user'].queryset = User.objects.exclude(id__in=useronboard)
    
    user = UserChoiceField(queryset=User.objects.all(), 
                    )
    class Meta:
        fields = ['Benutzer']
        widgets = {
            'user': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
        }
        labels = {
            'user': 'User',
        }



        

class ProzessEntryForm(ModelForm):
    class Meta:
        model = ProzessEntry
        fields = ['stelle', 'kunde', 'revenue', 'prozess_von', 'prozess_von_zwei']
        widgets = {
            'stelle': forms.TextInput(attrs={'class': 'form-control'}),
            'kunde': forms.TextInput(attrs={'class': 'form-control'}),
            'revenue': forms.NumberInput(attrs={'class': 'form-control', 'max':'99999'}),
            'prozess_von': forms.Select(attrs={'class': 'form-control selectpicker', 'data-live-search': 'true'}),
            'prozess_von_zwei': forms.Select(attrs={'class': 'form-control selectpicker', 'data-live-search': 'true'}),
        }
        labels = {
            'stelle': 'Stelle',
            'kunde': 'Kunde',
            'revenue': 'Umsatz in €',
            'prozess_von': 'Prozess von',
            'prozess_von_zwei': 'Zweite Person im Prozess',
        }

class OfferEntryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.boardid = kwargs.pop('boardid')
        super(OfferEntryForm, self).__init__(*args, **kwargs)
        board = InterviewBoard.objects.get(id=self.boardid)
        useronboard = InterviewBoardEntry.objects.filter(board=board).values_list('user__id', flat=True)
        #get unique users on board only
        self.fields['offer_von'].queryset = User.objects.filter(id__in=useronboard)
        self.fields['offer_von'].widget.attrs.update({'class': 'form-control selectpicker', 'data-live-search': 'true'})
        self.fields['offer_von_zwei'].widget.attrs.update({'class': 'form-control selectpicker', 'data-live-search': 'true'})
        self.fields['offer_von_zwei'].label = 'Zweite Person im Prozess'
        self.fields['offer_von_zwei'].required = False
    offer_von = UserChoiceFieldSingle(queryset=User.objects.all(),)
    offer_von_zwei = UserChoiceFieldSingle(queryset=User.objects.all(),)


    class Meta:
        model = Offer
        fields = ['stelle', 'kunde','kandidat', 'revenue', 'offer_von', 'offer_von_zwei']
        widgets = {
            'stelle': forms.TextInput(attrs={'class': 'form-control'}),
            'kunde': forms.TextInput(attrs={'class': 'form-control'}),
            'revenue': forms.NumberInput(attrs={'class': 'form-control','max':'99999'}),
            'kandidat': forms.TextInput(attrs={'class': 'form-control'}),
            'offer_von': forms.Select(attrs={'class': 'form-control selectpicker', 'data-live-search': 'true'}),
            'offer_von_zwei': forms.Select(attrs={'class': 'form-control selectpicker', 'data-live-search': 'true'}),
        }
        labels = {
            'stelle': 'Stelle',
            'kunde': 'Kunde',
            'revenue': 'Umsatz in €',
            'offer_von': 'Prozess von',
            'offer_von_zwei': 'Zweite Person im Prozess',
        }

class ToolKostenRechnungForm(ModelForm):
    class Meta:
        model = ToolKostenRechnung
        fields = ['rechnung_fuer']
        widgets = {
            'rechnung_fuer': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
        }

class RechnungsDatenForm(ModelForm):
    class Meta:
        model = RechnungsDaten
        fields = ['firmenname', 'strasse' ,'hausnummer','plz', 'ort']
        widgets = {
            'firmenname': forms.TextInput(attrs={'class': 'form-control'}),
            'strasse': forms.TextInput(attrs={'class': 'form-control'}),
            'hausnummer': forms.TextInput(attrs={'class': 'form-control'}),
            'plz': forms.TextInput(attrs={'class': 'form-control'}),
            'ort': forms.TextInput(attrs={'class': 'form-control'}),
        }




class AddUserToInvoice(forms.Form):
    user = UserChoiceField(queryset=User.objects.all(), 
                    )
    class Meta:
        fields = ['Benutzer']
        widgets = {
            'user': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
        }
        labels = {
            'user': 'User',
        }