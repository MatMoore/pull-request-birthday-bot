# coding=utf-8
import random
import requests
import tweepy
import inflect
from dateutil.relativedelta import relativedelta
from os import environ
from string import Template
from datetime import datetime

GITHUB = 'https://api.github.com'
MESSAGES = [
    Template(u"🎂🎂🎂 Happy $nth birthday $url !!! 🎂🎂🎂"),
    Template(u"Happy birthday $url 🎂 You are $n today!"),
    Template(u"$url is $n today! Woop woop! ⌨"),
    Template(u"Happy birthday $url 💾"),
    Template(u"Happy birthday to you! Happy birthday to you! Happy birthday dear $url, happy birthday to you! 💾"),
]


def matching_pull_requests(age):
    """
    Query all pull requests that are exactly $age years old.
    """
    today = datetime.utcnow().date()
    created = today - relativedelta(years=age)
    response = requests.get(GITHUB + '/search/issues?q=type:pr created:{:%Y-%m-%d} is:open'.format(created))
    return response.json()


def select_pull_request(age):
    """
    Pick a pull request that was created this day 1-5 years ago.
    """
    return random.choice(matching_pull_requests(age)['items'])


def generate_message(url, age):
    """
    Generate a message for a pull request.
    """
    template = random.choice(MESSAGES)
    nth = unicode(inflect.engine().ordinal(age))
    return template.substitute(url=url, n=unicode(age), nth=nth)


def load_twitter_auth():
    """
    Create a twitter OAuth handler based on the key set in the environment.
    """
    consumer_key = environ['TWITTER_CONSUMER_KEY']
    consumer_secret = environ['TWITTER_CONSUMER_SECRET']
    return tweepy.OAuthHandler(consumer_key, consumer_secret)


def fetch_twitter_access_token():
    """
    Interactively grant the app access to a twitter account via OAuth.

    The access token is valid until the user revokes it.

    Set these variables in the app's environment.
    """
    auth = load_twitter_auth()

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

    print 'TWITTER_ACCESS_KEY:    ' + auth.access_token
    print 'TWITTER_ACCESS_SECRET: ' + auth.access_token_secret


def tweet(message):
    """
    Post a message on the bot's twitter
    """
    auth = load_twitter_auth()
    key = environ['TWITTER_ACCESS_KEY']
    secret = environ['TWITTER_ACCESS_SECRET']
    auth.set_access_token(key, secret)
    api = tweepy.API(auth)
    api.update_status(message)
    print message


def activate():
    """
    Do the thing.
    """
    age = random.randint(1,5)
    pr = select_pull_request(age)
    url = pr['pull_request']['html_url']
    message = generate_message(url, age)
    tweet(message)


if __name__ == '__main__':
    activate()
