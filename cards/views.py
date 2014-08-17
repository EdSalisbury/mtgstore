# MTGStore
# (c)2014 Ed Salisbury
# See /LICENSE.txt for license

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse
from cards.models import Card, Edition
from django.template import Context
from slugify import slugify
from django import forms
import requests
import json


def user_login(request):
    auth = {}
    auth['authenticated'] = False
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])
        if user is not None:
            auth['authenticated'] = True
            auth['username'] = user.username
            login(request, user)

    response = json.dumps(auth)

    return HttpResponse(response)


def user_logout(request):
    logout(request)

    return HttpResponse("")


class CardForm(forms.Form):
    name = forms.CharField(max_length=30)
    condition = forms.CharField()
    edition = forms.CharField()
    quantity = forms.CharField()
    foil = forms.CharField()


def index(request):
    cards = Card.objects.all().order_by('name', 'edition')
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            edition = Edition.objects.get(set_id=form.cleaned_data['edition'])

            foil = False
            if (('foil' in form.cleaned_data and
                 form.cleaned_data['foil'] == 'true')):
                foil = True

            try:
                card = Card.objects.get(
                    name=form.cleaned_data['name'],
                    foil=foil,
                    edition=edition,
                    condition=form.cleaned_data['condition'])

                card.quantity += int(form.cleaned_data['quantity'])
                card.save()
            except Card.DoesNotExist:
                card = Card(
                    name=form.cleaned_data['name'],
                    edition=edition,
                    foil=foil,
                    condition=form.cleaned_data['condition'],
                    quantity=form.cleaned_data['quantity'])
                card.save()

                url = ('https://api.deckbrew.com/mtg/cards/%s' %
                       slugify(card.name))

                response = requests.get(url)
                editions = response.json()['editions']
                for edition in editions:
                    if ((edition['set_id'] == card.edition.set_id and
                         'price' in edition)):
                        card.multiverse_id = edition['multiverse_id']
                        card.rarity = edition['rarity'][0].upper()
                        card.price_low = edition['price']['low'] / 100.0
                        card.price_med = edition['price']['median'] / 100.0
                        card.price_high = edition['price']['high'] / 100.0

                        card.save()

    form = CardForm()

    context = Context({
        'card_list': cards,
        'form': form
    })

    return render(request, 'index.html', context)
