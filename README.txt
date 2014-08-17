=========
MTG Store
=========

Makes listing Magic: The Gathering cards on eBay much easier.  Utilizes the
eBay SDK, Django, and the Deckbrew API.

This is meant to be a starting point for your own project -- it could be
theoretically used out of the box, but most likely you will want to edit to
suit your needs.  It probably has issues, and I assume no responsibility,
yadda yadda.  Use at your own risk, your mileage may vary, etc. etc.

Installation:

$ pip install -r requirements.txt

Set up database:
mysql> create database mtgstore;
mysql> create user 'mtgstore'@'localhost' identified by 'PASSWORD';
mysql> grant all privileges on mtgstore.* to 'mtgstore'@'localhost';
mysql> flush privileges;

Set up config files:
$ cp ebay.yaml.orig ebay.yaml (Edit and add your eBay IDs)
$ cd mtgstore; cp settings.py.orig settings.py (Edit and set mysql password)

Set up webserver: (https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/modwsgi/)

Set up Django:
$ ./manage.py syncdb
$ ./manage.py migrate
$ ./manage.py collectstatic

$ sudo touch /var/log/mtgstore.log

Important: Update cards/management/commands/list_cards.py with your info - things
like your PayPal email address are stored here.

Usage:
Run ./manage.py update_editions to add all of the MTG sets
Log in to the website using the admin login you created when you ran syncdb
Add a card
Run ./manage.py list_cards

Notes:
Cards are listed asyncronously, and will update when you run list_cards.
You'll probably want to add list_cards and update_editions to a nightly crontab.

