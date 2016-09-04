# Pull request birthday bot

A twitter bot that wishes pull requests happy birthday if they're still open N years after they were created.

https://twitter.com/PR_birthday_bot

## Getting Started

To set up on a local machine for development/testing:

1. [Set up an app](http://blog.mollywhite.net/twitter-bots-pt2/) for your twitter developer account.

2. Set `TWITTER_CONSUMER_KEY` and `TWITTER_CONSUMER_SECRET` environment variables using the keys twitter gives you. E.g. run `export TWITTER_CONSUMER_KEY=blablabla` in your shell.

3. Grant the app access to your twitter account. There's a button for this in the twitter settings. To grant access to a different account you can hack `birthdaybot.py` to run the `fetch_twitter_access_token` function.

4. Set `TWITTER_ACCESS_KEY` and `TWITTER_ACCESS_SECRET` environment variables with the values from step 3.

5. Run `python birthdaybot/birthdaybot.py`

### Prerequisities

* Python 2
* pip

```
pip install requirements.txt
```

## Deployment

First [create a heroku app and push the repo to heroku](https://devcenter.heroku.com/articles/getting-started-with-python#introduction). It will complain about a missing Procfile but it's not needed.

The rest you can do either through the heroku web interface or the cli:

* [set the four twitter environment variables described above](https://devcenter.heroku.com/articles/getting-started-with-python#define-config-vars)
* [add the heroku scheduler plugin to the app](https://devcenter.heroku.com/articles/scheduler)
* add a job to the scheduler plugin. It should run `./bin/birthdaybot.py`

## Contributing

* Feel free to raise PRs and issues
* I will try and respond to things within a year
* Check the PRs the bot tweets about and see if you can get one resolved

## License

          DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                      Version 2, December 2004

    Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

    Everyone is permitted to copy and distribute verbatim or modified
    copies of this license document, and changing it is allowed as long
    as the name is changed.

               DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
      TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

     0. You just DO WHAT THE FUCK YOU WANT TO.
