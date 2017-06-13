import datetime
import tweepy
from dateutil.parser import parse
from get_mongo_client import get_mongo_client

from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings


def make_shows(db, theater, day):
    recent = datetime.datetime.now() - datetime.timedelta(hours=6)
    shows = {}
    return db.shows_latest.find(
            {'theater': theater, 'date': day},
            sort=[('start_time', 1)]
    )


def index(request):
    db = get_mongo_client().kinpri_theater_checker
    last_updated = db.theaters.find().sort(
        [('last_updated', -1)]).limit(1)[0]['last_updated']
    today = datetime.datetime.fromordinal(datetime.date.today().toordinal())
    day_num = 4
    days = [today + datetime.timedelta(days=i) for i in range(day_num)]
    theater_shows = [(theater,
                      [make_shows(db, theater['name'], day) for day in days])
                     for theater in db.theaters.find()]
    support_theater_num = len(db.shows_latest.distinct('theater'))
    present_total_theater_num = db.theaters.find({'start_date': parse('6/10')}).count()
    total_theater_num = db.theaters.find().count()
    return render(request, 'kinpri_theater_checker/index.html', {
        'last_updated': last_updated,
        'days': days,
        'theater_shows': theater_shows,
        'support_theater_num': support_theater_num,
        'total_theater_num': total_theater_num,
        'present_total_theater_num': present_total_theater_num,
    })

def theater(request):
    pass
