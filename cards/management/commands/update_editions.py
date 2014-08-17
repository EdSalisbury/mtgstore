# MTGStore
# (c)2014 Ed Salisbury
# See /LICENSE.txt for license

import requests
from django.core.management.base import BaseCommand
from cards.models import Edition

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = ''
    help = 'Updates list of editions'

    def handle(self, *args, **options):
        url = 'https://api.deckbrew.com/mtg/sets'
        response = requests.get(url)
        for item in response.json():
            try:
                Edition.objects.get(set_id=item['id'])
            except Edition.DoesNotExist:
                Edition.objects.create(
                    name=item['name'],
                    set_id=item['id'])

        logger.info("Editions updated successfully.")
