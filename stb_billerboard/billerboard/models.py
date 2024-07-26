from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Kontakt(models.Model):
    GENDER_CHOICES = [
        ('Herr', 'Herr'),
        ('Frau', 'Frau'),

    ]
    anrede = models.CharField(choices=GENDER_CHOICES, max_length=200, null=True, blank=True)
    position = models.CharField(max_length=200, null=True, blank=True)
    vorname = models.CharField(max_length=200, null=True, blank=True)
    nachname = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    telefon = models.CharField(max_length=200, null=True, blank=True)
    kontakt_added_at = models.DateTimeField(auto_now_add=True)
    kontakt_updated_at = models.DateTimeField(auto_now=True)
    kontakt_hubspotid = models.CharField(max_length=200, null=True, blank=True)
    eingetragen_von = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='kontakt_eingetragen_von')
    doer = models.CharField(max_length=200, null=True, blank=True)
    ist_ansprechpartner = models.BooleanField(default=False)
    def __str__(self):
        if self.vorname and self.nachname and self.anrede:

            return self.anrede+ ' ' + self.vorname + ' ' + self.nachname
        if self.anrede and self.nachname:
            return self.anrede+' '+self.nachname
        if self.vorname and self.nachname:
            return self.vorname + ' ' + self.nachname
        return 'Fehlerhafter Kontakt ' + str(self.id)
        


class Kandidat(models.Model):
    kontakt = models.ForeignKey(Kontakt, on_delete=models.CASCADE, null=True, blank=True)
    kandidat_added_at = models.DateTimeField(auto_now_add=True)
    berufsbezeichnung = models.CharField(max_length=200, null=True, blank=True)


    def __str__(self):
        return self.kontakt.vorname + ' ' + self.kontakt.nachname + ' (' + self.berufsbezeichnung + ')'

class Unternehmen(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    kontakte = models.ManyToManyField(Kontakt, blank=True, related_name='alle_kontakte')
    unternehmen_added_at = models.DateTimeField(auto_now_add=True)
    unternehmen_updated_at = models.DateTimeField(auto_now=True)
    unternehmen_hubspotid = models.CharField(max_length=200, null=True, blank=True)
    website = models.CharField(max_length=2000, null=True, blank=True)
    plz = models.CharField(max_length=200, null=True, blank=True)
    strasse_hausnummer = models.CharField(max_length=500, null=True, blank=True)
    ort = models.CharField(max_length=200, null=True, blank=True)
    telefon = models.CharField(max_length=200, null=True, blank=True)


    class Meta:
        verbose_name_plural = 'Unternehmen'
        unique_together = ('name', 'ort')

    def __str__(self):

        if self.ort:
            return self.name + ' (' + self.ort + ')'
        if self.name:
            return self.name
        #return str(self.name) + (' (' + str(self.ort) + ')') or ''

        return f'Fehlerhaftes Unternehmen {self.id}'
    
    def alle_deals(self):
        deals = Deal.objects.filter(unternehmen=self).count()
        return deals
    @property
    def ist_partnerunternehmen(self):
        if PartnerUnternehmen.objects.filter(unternehmen=self).exists():
            return True
        else:
            return False
    @property
    def ist_blacklisted(self):
        if BlacklistUnternehmen.objects.filter(unternehmen=self).exists():
            return True
        else:
            return False

class PartnerUnternehmen(models.Model):
    konditionen = models.TextField(null=True, blank=True)
    partnerunternehmen_added_at = models.DateTimeField(auto_now_add=True)
    partnerunternehmen_updated_at = models.DateTimeField(auto_now=True)
    partnerunternehmen_hubspotid = models.CharField(max_length=200, null=True, blank=True)
    unternehmen = models.ForeignKey(Unternehmen, on_delete=models.CASCADE, blank=True, null=True, related_name='partnerunternehmen')
    partnerunternehmen_added_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='partnerunternehmen_added_by')
    partnerunternehmen_updated_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='partnerunternehmen_updated_by')

class BlacklistUnternehmen(models.Model):
    blacklist_added_at = models.DateTimeField(auto_now_add=True)
    blacklist_updated_at = models.DateTimeField(auto_now=True)
    unternehmen = models.ForeignKey(Unternehmen, on_delete=models.CASCADE, blank=True, null=True, related_name='blacklistunternehmen')
    blacklist_added_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='blacklist_added_by')
    blacklist_updated_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='blacklist_updated_by')
    grund = models.TextField(null=True, blank=True)




class SalesStufe(models.Model):
    prozente = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=5)
    name = models.CharField(max_length=200, null=True, blank=True)
    salesstufe_added_at = models.DateTimeField(auto_now_add=True)
    salesstufe_updated_at = models.DateTimeField(auto_now=True)
    revenue_min = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)

class ProvisionLayer(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    layer_above = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    prozente = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=5)
    name = models.CharField(max_length=200, null=True, blank=True)
    provisionlayer_added_at = models.DateTimeField(auto_now_add=True)
    provisionlayer_updated_at = models.DateTimeField(auto_now=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    manager_prozente = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=5)

class DealDaten(models.Model):
    DATEN_CHOICES = [
        ('AGB', 'AGB vom Kunden'),
        ('DSGVO', 'DSGVO vom Kandidaten'),
        ('VERTRAG', 'Vertrag unterschrieben von beiden Parteien'),
        ('SERVICEABRECHNUNG', 'Serviceabrechnung'),
        ('SONSTIGES', 'Sonstiges')

    ]
    name = models.CharField(max_length=200, choices=DATEN_CHOICES)
    datei = models.FileField(upload_to='uploads/beweisgrundlage', null=True, blank=True)
    deal = models.ForeignKey('Deal', on_delete=models.CASCADE, blank=True, null=True)
    dealDaten_added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + ' - ' + str(self.deal) + ' (' + str(self.deal.deal_closed_at) + ')' + ' - ' + str(self.deal.user)

class Deal(models.Model):
    QUELLENCA_CHOICES = [
        ('JOIN', 'Join'),
        ('LINKEDIN', 'LinkedIn'),
        ('XING', 'Xing'),
        ('EMPFEHLUNG', 'Empfehlung'),
        ('MARKETING', 'Marketing / Ads'),
        ('SONSTIGES', 'Sonstiges')]
    
    QUELLENKU_CHOICES = [
        ('COLDCALL', 'Coldcall'),
        ('SHOT', 'E-Mail Sequenz'),
        ('SNIPER', 'Sniper Shot'),
        ('XING', 'Xing'),
        ('LINKEDIN', 'LinkedIn'),
        ('EMPFEHLUNG', 'Empfehlung'),
        ('BESTANDSKUNDE', 'Bestandskunde'),
        ('SONSTIGES', 'Sonstiges')]


    deal_added_at = models.DateTimeField(auto_now_add=True)
    deal_updated_at = models.DateTimeField(auto_now=True)
    deal_closed_at = models.DateField(null=True, blank=True)
    deal_hubspotid = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    kandidat = models.ForeignKey(Kandidat, on_delete=models.CASCADE, blank=True, null=True)
    unternehmen = models.ForeignKey(Unternehmen, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    antrittsdatum = models.DateField(null=True, blank=True)
    kulanz_bis = models.DateField(null=True, blank=True)
    genehmigt_von = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='genehmigt_von')
    genehmigt = models.BooleanField(default=False)
    kandidat_von = models.CharField(max_length=200, choices=QUELLENCA_CHOICES, null=True, blank=True)
    unternehmen_von = models.CharField(max_length=200, null=True, blank=True, choices=QUELLENKU_CHOICES)
    bonding_mail = models.BooleanField(default=False)
    abteilung = models.ForeignKey('userauth.Abteilung', on_delete=models.CASCADE, blank=True, null=True)
    storniert = models.BooleanField(default=False)
    storniert_am = models.DateField(null=True, blank=True)
    storniert_von = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='storniert_von')


    def auszahlungssumme(self):
        auszahlungen = Auszahlung.objects.filter(deal=self)
        summe = 0
        for auszahlung in auszahlungen:
            summe += auszahlung.amount
        return summe
    
    def beweisgrundlagecheck(self):
        if DealDaten.objects.filter(deal=self).exists():
            return True
        else:
            return False
    def beweisgrundlage(self):
        dealDaten = DealDaten.objects.filter(deal=self)
        return dealDaten
    
    def shares(self):
        shares = Share.objects.filter(deal=self)
        return shares

    def __str__(self):
        try:
            return self.unternehmen.name + ' - ' + self.kandidat.kontakt.vorname + ' ' + self.kandidat.kontakt.nachname + ' (' + str(self.amount) + '€)'
        except:
            return 'Fehlerhafter Deal ' + str(self.id)
    class Meta:
        unique_together = ('kandidat', 'unternehmen')

class Share(models.Model):
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, null=True, blank=True, related_name='share')
    share_added_at = models.DateField(auto_now_add=True)
    share_genehmigt_von = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='share_genehmigt_von')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    prozente = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=5)


    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + ' (' + str(self.prozente) + '%)' 
class Einzahlung(models.Model):
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, null=True, blank=True)
    einzahlung_added_at = models.DateTimeField(auto_now_add=True)
    rechnungsnummer = models.CharField(max_length=200, null=True, blank=True)
    amount = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    eingetragen_von = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='eingetragen_von')


class Auszahlung(models.Model):
    AUSZAHLUNGS_CHOICES = [
        ('DEAL', 'Deal'),
        ('SONSTIGES', 'Sonstiges'),
    ]
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, null=True, blank=True)
    auszahlung_added_at = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    auszahlungstyp = models.CharField(max_length=200, null=True, blank=True, choices=AUSZAHLUNGS_CHOICES)
    autorisiert_von = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='autorisiert_von')
    ausgezahlt_an = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='ausgezahlt_an')


class Incentive(models.Model):
    name = models.CharField(max_length=250)
    beschreibung = models.TextField(null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_global = models.BooleanField(default=False)
    goal = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)

    def __str__(self):
        return self.name + ' (' + str(self.start_date) + ' - ' + str(self.end_date) + ')'

class Umsatzziel(models.Model):
    date = models.DateField()
    amount = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)

    def __str__(self):
        return str(self.date) + ' - ' + str(self.amount) + '€'
    

class InterviewBoard(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        try:
            if self.name:
                return self.name
            else:
                return 'Board ohne Name'
        except:
            return 'Board ohne Name'

class InterviewBoardEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    board = models.ForeignKey(InterviewBoard, on_delete=models.CASCADE, blank=True, null=True)
    iv_heute = models.IntegerField(null=True, blank=True, default = 0)
    iv_this_week = models.IntegerField(null=True, blank=True, default = 0)
    iv_next_week = models.IntegerField(null=True, blank=True, default = 0)
    offer = models.IntegerField(null=True, blank=True, default = 0)
    revenue = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10, default = 0)
    ist_aktuell = models.BooleanField(default=True)
    entry_added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        try:
            return str(self.user) + ' - ' + str(self.board)
        except:
            return str(self.user)


class ProzessEntry(models.Model):
    eingetragen_von = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='eingetragen_von_prozess')
    prozess_added_at = models.DateTimeField(auto_now_add=True)
    stelle = models.CharField(max_length=200)
    kunde = models.CharField(max_length=200, null=True, blank=True)
    revenue = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    prozess_von = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='prozess_von')
    prozess_von_zwei = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='prozess_von_zwei')
    ist_abgeschlossen = models.BooleanField(default=False)
    abgeschlossen_am = models.DateField(null=True, blank=True)
    won = models.BooleanField(default=False)
    lost = models.BooleanField(default=False)

    def __str__(self):
        try:
            return self.stelle + ' - ' + self.kunde + ' (' + str(self.revenue) + '€)'
        except:
            return 'Fehlerhafter Prozess ' + str(self.id)

class Offer(models.Model):
    offer_added_at = models.DateTimeField(auto_now_add=True)
    offer_updated_at = models.DateTimeField(auto_now=True)
    stelle = models.CharField(max_length=200)
    kunde = models.CharField(max_length=200, null=True, blank=True)
    kandidat = models.CharField(max_length=200, null=True, blank=True)
    revenue = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    offer_von = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offer_von')
    offer_von_zwei = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='offer_von_zwei')
    ist_abgeschlossen = models.BooleanField(default=False)
    abgeschlossen_am = models.DateField(null=True, blank=True)
    won = models.BooleanField(default=False)
    lost = models.BooleanField(default=False)
    board = models.ForeignKey(InterviewBoard, on_delete=models.CASCADE, blank=True, null=True)
    lost_reason = models.TextField(null=True, blank=True)
    def __str__(self):
        try:
            return self.stelle + ' - ' + self.kunde + ' (' + str(self.revenue) + '€)'
        except:
            return 'Fehlerhaftes Offer ' + str(self.id)

class Tool(models.Model):
    toolname = models.CharField(max_length=200)
    tool_added_at = models.DateTimeField(auto_now_add=True)
    kosten = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)

    def __str__(self):
        return self.toolname
class ToolKostenRechnung(models.Model):
    tools = models.ManyToManyField(Tool, blank=True, related_name='toolkostenrechnung')
    rechnungsnummer = models.CharField(max_length=200, null=True, blank=True)
    gesamtsumme = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    toolkostenrechnung_added_at = models.DateTimeField(auto_now_add=True)
    toolkostenrechnung_updated_at = models.DateTimeField(auto_now=True)
    rechnung_fuer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='rechnung_fuer')
    bezahlt = models.BooleanField(default=False)
    bezahlt_am = models.DateField(null=True, blank=True)
    genehmigt = models.BooleanField(default=False)
    genehmigt_am = models.DateField(null=True, blank=True)
    lexoffice_id = models.CharField(max_length=200, null=True, blank=True)
    rechnungsdatum = models.DateField(auto_now_add=True)

class DailySurveyQuestion(models.Model):
    data = models.TextField()
    level = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.data


class DailySurveyAnswer(models.Model):
    data = models.TextField()
    question = models.ForeignKey(DailySurveyQuestion, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dailySurvey = models.ForeignKey('DailySurvey', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.data


class DailySurvey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'Survey by {self.user}'
