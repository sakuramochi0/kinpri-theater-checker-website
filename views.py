import datetime
import tweepy
from dateutil.parser import parse
from get_mongo_client import get_mongo_client

from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings


def make_shows(db, theater, day):
    shows = {}
    for show in db.shows.find(
        {'theater': theater, 'date': day},
        sort=[('updated', -1)]
    ):
        key = (show['start_time'], show['title'], show['theater'])
        if key in shows:
            continue
        shows[key] = show
    shows = [show for _, show in sorted(shows.items())]
    return shows


def index(request):
    db = get_mongo_client().kinpri_theater_checker
    #today = datetime.datetime.fromordinal(datetime.date.today().toordinal())
    today = parse('6/9')
    day_num = 4
    days = [today + datetime.timedelta(days=i) for i in range(day_num)]
    return render(request, 'kinpri_theater_checker/index.html', {
        'last_updated': db.theaters.find().sort([('last_updated', -1)]).limit(1)[0]['last_updated'],
        'days': days,
        'theater_shows': [(
            theater,
            [make_shows(db, theater['name'], day) for day in days]
        ) for theater in db.theaters.find()],
    })

def theater(request):
    pass
