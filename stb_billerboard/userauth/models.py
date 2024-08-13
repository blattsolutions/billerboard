from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from billerboard.models import Deal
from django.utils import timezone
from dateutil.relativedelta import relativedelta

# Create your models here.

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        if not Rang.objects.filter(name='Silber').exists():
            Rang.objects.create(name='Silber', aufstieg_bei=22000)
        RangHistory.objects.create(user=instance.profile, rang=Rang.objects.get(name='Silber'))
    instance.profile.save()

class CompanyRole(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    role_added_at = models.DateTimeField(auto_now_add=True)
    role_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    


class Profile(models.Model):

    TOOLABRECHNUNG_CHOICES = [
        ('1', 'Monatlich'),
        ('3', 'Quartalsweise'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    team_lead = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='team_lead')
    role = models.ForeignKey(CompanyRole, on_delete=models.CASCADE, null=True, blank=True)
    abteilung = models.ForeignKey('Abteilung', on_delete=models.SET_NULL, null=True, blank=True)
    last_rang_update = models.DateTimeField(default=timezone.now)
    ist_aktiv = models.BooleanField(default=True)
    toolabrechnungszyklus = models.CharField(max_length=1, choices=TOOLABRECHNUNG_CHOICES, default='1')
    minrang = models.ForeignKey('Rang', on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        try:
            return self.user.first_name + " " + self.user.last_name + " - " + self.role.name + " - " + self.abteilung.name
        except:
            return self.user.first_name + " " + self.user.last_name + " - " + 'Keine Rolle'
    @property
    def get_rang(self):
        return RangHistory.objects.filter(user=self).order_by('-rang_updated_at').first().rang.name

class Rang(models.Model):

    name = models.CharField(max_length=200, null=True, blank=True)
    aufstieg_bei = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    abstieg_bei = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    next_rang = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='higher_rang')
    previous_rang = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='lower_rang')
    
    def __str__(self):
        return self.name
    

class RangHistory(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='rang_history')
    rang = models.ForeignKey(Rang, on_delete=models.CASCADE)
    rang_updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.user.first_name + " " + self.user.user.last_name + " - " + self.rang.name + " - " + str(self.rang_updated_at)
class Abteilung(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    icon = models.CharField(max_length=200, null=True, blank=True)
    farbe = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

class RechnungsDaten(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rechnungsdaten')
    firmenname = models.CharField(max_length=200)
    strasse = models.CharField(max_length=200)
    hausnummer = models.CharField(max_length=200)
    plz = models.CharField(max_length=200)
    ort = models.CharField(max_length=200)