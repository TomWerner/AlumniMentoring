# Iowa Alumni Mentoring

## Running locally
```sh
$ pip install -r requirements.txt
$ npm install bower
$ bower install
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py loaddata starter_code.json
$ python manage.py loaddata starter_contest.json
$ python manage.py loaddata starter_rules.json
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
