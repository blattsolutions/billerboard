from typing import Any
from django.db import models
from django.contrib.auth.models import User
from billerboard.models import Kontakt, Unternehmen
from django.utils import timezone
import datetime
# Create your models here.

class ListenImport(models.Model):
    name = models.CharField(max_length=500)
    liste = models.FileField(upload_to='uploads/listen/', max_length=500)
    datum = models.DateTimeField(auto_now_add=True)
    erfolgreich = models.BooleanField(default=False)
    neue_kontakte = models.IntegerField(default=0)
    neue_unternehmen = models.IntegerField(default=0)
    fuer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='fuer')
    hochgeladen_von = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='hochgeladen_von')
    grund = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.liste.name.replace('uploads/', '')
    
class Liste(models.Model):
    import_liste = models.OneToOneField(ListenImport, on_delete=models.CASCADE, blank=True, null=True, related_name='import_liste')
    finished = models.DateTimeField(blank=True, null=True)
    
    @property
    def anzahl_unternehmen(self):
        #print(ListAssignment.objects.filter(liste=self)).count()
        return ListAssignment.objects.filter(liste=self).count()
    @property
    def anzahl_completed(self):
        return ListAssignment.objects.filter(liste=self, kontakt__isnull=False, unternehmen__isnull=False).count()
class ListAssignment(models.Model):
    liste = models.ForeignKey(Liste, on_delete=models.CASCADE, blank=True, null=True, related_name='liste')
    kontakt = models.ForeignKey('billerboard.Kontakt', on_delete=models.CASCADE, blank=True, null=True, related_name='kontakt')
    unternehmen = models.ForeignKey('billerboard.Unternehmen', on_delete=models.CASCADE, blank=True, null=True, related_name='unternehmen')
    offene_stellen = models.IntegerField(default=1)
    def __str__(self):
        return str(self.liste.import_liste) + ' ' + str(self.unternehmen)
    @property
    def is_complete(self):
        if self.kontakt and self.unternehmen:
            return True
        else:
            return False
class Entry(models.Model):
    listassignment = models.ForeignKey(ListAssignment, on_delete=models.CASCADE, blank=True, null=True)
    unternehmen = models.ForeignKey('billerboard.Unternehmen', on_delete=models.CASCADE, blank=True, null=True)
    kontakt = models.ForeignKey('billerboard.Kontakt', on_delete=models.CASCADE, blank=True, null=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='assigned_to')
    time_started = models.DateTimeField(null=True, blank=True)
    time_finished = models.DateTimeField(null=True, blank=True)
    skipped = models.DateTimeField(null=True, blank=True)
    on_hold = models.DateTimeField(null=True, blank=True)
    rate = models.ForeignKey('EntryRate', on_delete=models.CASCADE, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    def __str__(self):
        return str(self.unternehmen) + ' ' + str(self.assigned_to)
    skip_count = models.IntegerField(default=0)
    @property
    def skip(self):
        if self.assigned_to.dataentryprofile.available_skips <= 0:
            return False
        else:
            self.skipped = timezone.now()
            self.skip_count += 1
            self.save()
            self.assigned_to.dataentryprofile.available_skips -= 1
            self.assigned_to.dataentryprofile.lifetime_skips += 1
            self.assigned_to.dataentryprofile.save()
            return True
    @property
    def hold(self):
        self.on_hold = timezone.now()
        self.assigned_to.dataentryprofile.lifetime_hold += 1
        self.assigned_to.dataentryprofile.save()
        self.save()
    def start(self):
        self.started_at = timezone.now()
        self.save()
        return True
    
    @property
    def get_timer(self):
        print('get_timer')
        if self.time_started and not self.time_finished:
            if timezone.now() > (self.time_started + datetime.timedelta(minutes=10)):
                return 0
            else:
                delta = (self.time_started + datetime.timedelta(minutes=15)) - timezone.now()
                print(delta)
                return delta.total_seconds()
        return 0


class EntryRate(models.Model):
    rate = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=5, default=0.15)
    def __str__(self):
        return str(self.rate)
class DataEntryProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='dataentryprofile')
    rate = models.ForeignKey('EntryRate', on_delete=models.CASCADE, blank=True, null=True)
    current_working = models.ForeignKey('Entry', on_delete=models.CASCADE, blank=True, null=True)
    available_skips = models.IntegerField(default=10)
    lifetime_skips = models.IntegerField(default=0)
    lifetime_completed = models.IntegerField(default=0)
    lifetime_hold = models.IntegerField(default=0)

    @property
    def on_hold(self):
        return Entry.objects.filter(assigned_to=self.user, on_hold__isnull=False)
    @property
    def on_hold_count(self):
        return Entry.objects.filter(assigned_to=self.user, on_hold__isnull=False).count()
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
    