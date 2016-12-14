# Iowa Alumni Mentoring

## Running locally
```sh
$ pip install -r requirements.txt
$ npm install bower
$ bower install
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py loaddata dummy_data.json  # Only do this for local testing!
$ python manage.py runserver
```

## Deploying to Heroku
```sh
$ git push heroku master
$ heroku run python manage.py migrate
$ heroku run python manage.py collectstatic

# First time only
$ heroku run python manage.py createsuperuser
```

## Things that need to be set for heroku
Under settings, config variables, you need to have GMAIL_USERNAME be the username of the gmail used to send
emails as invitations, approval confirmation, and announcement of a mentorship being formed. GMAIL_PASSWORD
should be set to the password of that account. Be sure that you have enabled less secure app access to this
account. (https://support.google.com/accounts/answer/6010255)

You will also want HOST_URL set to the hosting url, and SECRET_KEY set to a random very long string of
numbers and digits.

**BE SURE NEVER TO COMMIT THE SECRET KEY OR GMAIL PASSWORD TO GITHUB!!!**

To avoid that information from going into version control, they are part of the heroku setup. If heroku is
not being used, they should be in a local settings.py file. Whenever you're deployed to production,
run ```python manage.py check --deploy``` and make sure there are no issues.