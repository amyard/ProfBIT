from random import randrange
from datetime import timedelta, datetime

def random_date():
    start = datetime.strptime('01/01/2018 9:00', '%m/%d/%Y %I:%M')
    end = datetime.now()

    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)