from celery import shared_task
from .models import Profile, Rang, RangHistory
from billerboard.models import Deal, Share
from django.utils import timezone
from django.contrib.auth.models import User
from dateutil.relativedelta import relativedelta



@shared_task
def calculate_rang():
    
    last_month = timezone.now() - relativedelta(months=1)
    deals_last_month = Deal.objects.filter(deal_closed_at__month=last_month.month).filter(deal_closed_at__year=last_month.year)
    print(last_month)
    shares_last_month = Share.objects.filter(deal__in=deals_last_month)
    print(len(deals_last_month))
    print(len(shares_last_month))
    print(len(Profile.objects.all()))
    for profile in Profile.objects.all():
        print(profile.user)
        rev = 0
        current_rang = RangHistory.objects.filter(user=profile).order_by('-rang_updated_at').first()
        for deal in deals_last_month:
            if deal.user == profile.user:
                for share in Share.objects.filter(deal=deal):
                    if share.user != profile.user:
                        rev -= deal.amount * (share.prozente/100) 
                rev += deal.amount
        for share in shares_last_month:
            if share.user == profile.user:
                rev += share.prozente * share.deal.amount / 100
        
        print(f'Revenue: {rev}')
        if current_rang.rang.next_rang:
            if rev >= current_rang.rang.aufstieg_bei:# and (profile.last_rang_update.month != timezone.now().month):
                if current_rang.rang.next_rang:
                    
                    
                    r = RangHistory.objects.create(user=profile, rang=current_rang.rang.next_rang)
                    r.rang_updated_at = timezone.now()#-relativedelta(months=1)
                    r.save()
                    
                    print(f'Aufstieg:{profile.user} {current_rang.rang.name}')

                #else:
                #    print(f'Letztes update zu früh: {profile.last_rang_update}')
        if rev == 0:# and (profile.last_rang_update.month != timezone.now().month):
            if current_rang.rang.previous_rang:

                if current_rang.rang == profile.minrang:
                    r = RangHistory.objects.create(user=profile, rang=current_rang.rang)
                    r.rang_updated_at = timezone.now()#-relativedelta(months=1)
                    r.save()
                    print('Rangprotection')
                else:
                    r = RangHistory.objects.create(user=profile, rang=current_rang.rang.previous_rang)
                    r.rang_updated_at = timezone.now()#-relativedelta(months=1)
                    r.save()
                    print(f'Abstieg: {profile.user} {current_rang.rang.name}')
            else:
                print('Kein Abstieg möglich')

        profile.last_rang_update = timezone.now()#-relativedelta(months=1)
        print(f'Letztes update: {profile.last_rang_update}')
        profile.save()
        


        