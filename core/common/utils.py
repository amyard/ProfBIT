from random import randrange
from datetime import timedelta, datetime, time
from django.utils import timezone

# generate random date
def random_date():
    start = datetime.strptime('01/01/2018 9:00', '%m/%d/%Y %I:%M')
    end = datetime.now()
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)



def get_random_date(n):
    start = datetime.strptime('01/01/2018 9:00', '%m/%d/%Y %I:%M')
    aware_datetime = timezone.make_aware(start)
    res = aware_datetime + timedelta(hours=n)
    return res


def clean_date_for_orderbydateview(value):
    start_date = datetime.combine(value, time(00, 00))
    start = timezone.make_aware(start_date)
    return start


# get ip address
def get_ip_from_request(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
