from celery import shared_task
from time import sleep
from .models import InterviewBoardEntry, Deal
from django.utils import timezone
import datetime


@shared_task
def daily_iv_reset():
    entries = InterviewBoardEntry.objects.filter(ist_aktuell=True)
    #if monday reset all entries and copy to a new one
    if timezone.now().weekday() == 0:
        for entry in entries:
            entry.ist_aktuell = False
            entry.save()
            entry.pk = None
            entry.ist_aktuell = True
            entry.iv_heute = 0
            entry.iv_this_week = entry.iv_next_week
            entry.iv_next_week = 0
            entry.save()
    else:
        for entry in entries:
            entry.ist_aktuell = False
            entry.save()
            entry.pk = None
            entry.iv_heute = 0
            entry.entry_added_at = timezone.now()
            entry.ist_aktuell = True
            entry.save()


@shared_task
def daily_bonding_mail_check():
    deals = Deal.objects.filter(bonding_mail=False)
    for deal in deals:
        if deal.antrittsdatum:
            print("Deal: " + deal.user.email + " Antrittsdatum: " + str(deal.antrittsdatum) + " -7: " + str(deal.antrittsdatum - datetime.timedelta(days=7)) + " Now: " + str(timezone.now().date()))
            if deal.antrittsdatum - datetime.timedelta(days=7) == timezone.now().date():
                print("Send Bonding Mail to: " + deal.user.email)
                for share in deal.shares():
                    print("Send Bonding Mail to: " + share.user.email)
            else:
                print("No Bonding Mail to send to: " + deal.user.email)
                for share in deal.shares():
                    print("No Bonding Mail to send to: " + share.user.email)
