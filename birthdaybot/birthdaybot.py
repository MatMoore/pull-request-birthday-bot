# coding=utf-8
import json
import random
import tweepy
from dateutil.relativedelta import relativedelta
from inflect import engine
from requests import get
from os import environ
from string import Template
from datetime import datetime

_token = environ['ACCESS_TOKEN']
AUTH = dict(Authorization='token {}'.format(_token))
GITHUB = 'https://api.github.com'
MESSAGES = [
    Template(u"🎂🎂🎂 Happy $nth birthday $url !!! 🎂🎂🎂"),
    Template(u"Happy birthday $url 🎂 You are $n today!"),
    Template(u"$url is $n today! Woop woop! ⌨"),
    Template(u"Happy birthday $url 💾"),
    Template(u"Happy birthday to you! Happy birthday to you! Happy birthday dear $url, happy birthday to you! 💾"),
]


def matching_pull_requests(age):
    today = datetime.utcnow().date()
    created = today - relativedelta(years=age)
    print '/search/issues?q=type:pr created:{:%Y-%m-%d} is:open'.format(created)
    response = get(GITHUB + '/search/issues?q=type:pr created:{:%Y-%m-%d} is:open'.format(created))
    return response.json()


def select_pull_request():
    age = random.randint(1,5)
    return random.choice(matching_pull_requests(age)['items'])


def message(url, age):
    template = random.choice(MESSAGES)
    nth = unicode(engine().ordinal(age))
    return template.substitute(url=url, n=unicode(age), nth=nth)


def get_twitter_auth():
    consumer_key = environ['TWITTER_CONSUMER_KEY']
    consumer_secret = environ['TWITTER_CONSUMER_SECRET']
    return tweepy.OAuthHandler(consumer_key, consumer_secret)


def get_twitter_access_token():
    auth = get_twitter_auth()

    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print 'Error! Failed to get request token.'

    print 'Go to {} to grant access'.format(redirect_url)
    verifier = raw_input('Enter the code from twitter: ')

    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        print 'Error! Failed to get access token.'

    print 'Access token:  ' + auth.access_token
    print 'Access secret: ' + auth.access_token_secret


def tweet(message):
    auth = get_twitter_auth()
    key = environ['TWITTER_ACCESS_KEY']
    secret = environ['TWITTER_ACCESS_SECRET']
    auth.set_access_token(key, secret)
    api = tweepy.API(auth)
    api.update_status(message)
    print message


if __name__ == '__main__':
    pr = select_pull_request()
    url = pr['pull_request']['html_url']
    created = datetime.strptime(pr['created_at'], '%Y-%m-%dT%H:%M:%SZ')
    age = int(round((datetime.utcnow() - created).days / 365.0))
    message = message(url, age)
    tweet(message)
