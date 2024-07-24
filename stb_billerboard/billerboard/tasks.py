from celery import shared_task
from time import sleep
from .models import InterviewBoardEntry, Deal
from django.utils import timezone
import datetime
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

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
    d = Deal.objects.filter(bonding_mail=False)
    for b in d:
        if b.antrittsdatum:
            if b.antrittsdatum <= timezone.now().date():
                b.bonding_mail = True
                b.save()
                print('Date in past set Bonding true')
        else:
            b.bonding_mail = True
            b.save()
            print('No Date set Bonding true')
        
    deals = Deal.objects.filter(bonding_mail=False)
    for deal in deals:
        if deal.antrittsdatum:
            print("Deal: " + deal.user.email + " Antrittsdatum: " + str(deal.antrittsdatum) + " -7: " + str(deal.antrittsdatum - datetime.timedelta(days=7)) + " Now: " + str(timezone.now().date()))
            if deal.antrittsdatum - datetime.timedelta(days=7) == timezone.now().date():
                print("Send Bonding Mail to: " + deal.user.email)
                subject = f'Antritt deines Kandidaten {deal.kandidat.kontakt.vorname} {deal.kandidat.kontakt.nachname} bei {deal.unternehmen} steht bevor!'
                html_message = render_to_string('email/antritt_7_tage.html', {'deal': deal})
                plain_message = strip_tags(html_message)
                from_email = 'Stoneberg Billerboard <no-reply@stoneberg.work>'
                to = f'{deal.user.email}'
                mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

                
                for share in deal.shares():
                    print("Send Bonding Mail to: " + share.user.email)
                    to = f'{share.user.email}'
                mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                deal.bonding_mail = True
                deal.save()
