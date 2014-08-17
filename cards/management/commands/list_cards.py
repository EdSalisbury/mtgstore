# MTGStore
# (c)2014 Ed Salisbury
# See /LICENSE.txt for license

import json
import math
import cgi
import re
from decimal import Decimal
import requests
from slugify import slugify

from ebaysdk.trading import Connection as Trading
from ebaysdk.exception import ConnectionError

from django.core.management.base import BaseCommand
from cards.models import Card

import logging
logger = logging.getLogger(__name__)

# Paypal email address
PAYPAL_ADDRESS = ""

# Item Location
LOCATION = "Anytown, USA"

# Category for MTG Singles
CATEGORY_ID = 19115

# Cost for First Class Shipping (part of item price)
SHIPPING_COST = 2.00

# Cost for International First Class Shipping (additional)
INTL_SHIPPING = 4.00

# eBay Store Category ID
STORE_CATEGORY_ID = 5396962011

# Price multiplier - done after all adjustments
PRICE_MULT = 0.85

# Don't list anything for under this price
MIN_PRICE = 2.99

# Foil multiplier
FOIL_MULT = 3

# For cards in Excellent (EX) condition
EX_MULT = 0.9

# For cards in Very Good (VG) condition
VG_MULT = 0.8

# For cards in Good (G) condition
G_MULT = 0.7

# Don't automatically list any card if it's over this threshold
MAX_AUTO_LIST = 50

# Only needed if you're an eBay employee
EBAY_EMP = False

# Editions that are foil-only - needs to be updated with all of the sets that
# are foil only.  The deckbrew API does not have this info.
FOIL_SETS = ['CM1']


class Command(BaseCommand):
    args = ''
    help = 'Lists cards'

    def __init__(self):
        self.api = Trading()
        self.category_id = CATEGORY_ID
        super(Command, self).__init__()

    def handle(self, *args, **options):
        cards = Card.objects.all().order_by('name', 'edition')
        for card in cards:
            if card.quantity == 0:
                logger.info("Deleting %s as there are 0 quantity available"
                            % card)
                card.delete()
                continue

            url = 'https://api.deckbrew.com/mtg/cards/%s' % slugify(card.name)

            response = requests.get(url)
            try:
                editions = response.json()['editions']

            except KeyError:
                logger.warning("Card %s not found in Deckbrew database"
                               % card.name)
                continue

            for edition in editions:
                if ((edition['set_id'] == card.edition.set_id and
                     'price' in edition)):
                    card.multiverse_id = edition['multiverse_id']
                    card.rarity = edition['rarity'][0].upper()
                    card.price_low = edition['price']['low'] / 100.0
                    card.price_med = edition['price']['median'] / 100.0
                    card.price_high = edition['price']['high'] / 100.0

                    price = float(card.price_med)

                    if card.edition.set_id in FOIL_SETS:
                        card.foil = True

                    if card.foil and card.edition.set_id not in FOIL_SETS:
                        price *= FOIL_MULT

                    if card.condition == 'EX':
                        price *= EX_MULT
                    if card.condition == 'VG':
                        price *= VG_MULT
                    if card.condition == 'G':
                        price *= G_MULT

                    ebay_price = (Decimal(math.ceil((price + SHIPPING_COST) *
                                  PRICE_MULT) - 0.01))

                    if ebay_price < MIN_PRICE:
                        ebay_price = MIN_PRICE

                    if float(ebay_price) != float(card.ebay_price):
                        logger.info("Updating database price for %s from %.2f "
                                    "to %.2f" % (card, card.ebay_price,
                                                 ebay_price))
                        card.ebay_price = ebay_price

                    card.save()

            if card.multiverse_id:
                if card.ebay_item_id:
                    self.UpdateCard(card)
                elif card.quantity:
                    card.ebay_item_id = self.ListCard(card)
                    card.save()

    def UploadPhoto(self, multiverse_id, card_name):
        photo_data = {
            "WarningLevel": "Low",
            "ExternalPictureURL": ("http://mtgimage.com/multiverseid/%s.jpg"
                                   % multiverse_id),
            "PictureName": card_name
        }

        response = self.api.execute('UploadSiteHostedPictures', photo_data)
        data = json.loads(response.json())
        self.photo_url = data['SiteHostedPictureDetails']['FullURL']

    def GetListingData(self, card):

        name = card.name

        if card.foil:
            name += " FOIL"

        title = ("%s (%s) - %s %s - MTG Magic the Gathering" %
                 (name, card.edition, card.get_rarity_display(),
                  card.get_condition_display()))

        if len(title) > 80:
            title = ("%s (%s) - %s %s - MTG Magic" %
                     (name, card.edition, card.get_rarity_display(),
                      card.get_condition_display()))

        if len(title) > 80:
            title = ("%s (%s) - %s %s - MTG" %
                     (name, card.edition, card.get_rarity_display(),
                      card.get_condition_display()))

        if len(title) > 80:
            title = ("%s (%s) - %s %s" %
                     (name, card.edition, card.get_rarity_display(),
                      card.get_condition_display()))

        if len(title) > 80:
            logger.error("Cannot set title for %s, skipping" % card)
            return

        nm_desc = ("<b>NM (Near Mint/Mint):</b> Card is perfect or nearly "
                   "perfect. May have very slight edge or corner wear that is "
                   "noticeable only on close inspection.")
        ex_desc = ("<b>EX (Excellent):</b> Card has light play wear. May have "
                   " a few edge nicks or a lightly worn corner.")
        vg_desc = ("<b>VG (Very Good):</b> Card has moderate play wear. May "
                   "have multiple edge nicks and edge whitening.")
        g_desc = ("<b>G (Good):</b> Card has moderate to heavy play wear. "
                  "Whitening on all edges and probably on the surface. May "
                  "also contain light creasing.")

        description = ("<p>Photo is stock unless otherwise noted.</p>"
                       "<h1>Condition Guide:</h1>"
                       "<p>%s</p><p>%s</p><p>%s</p><p>%s</p>" %
                       (nm_desc, ex_desc, vg_desc, g_desc))

        description += ("<h1>Shipping:</h1><ul>"
                        "<li>Cards are shipped securely in sleeves, plastic "
                        "top loaders/boxes and in bubble mailers.</li>"
                        "<li>Domestic shipping is FREE for USPS First "
                        "Class</li>"
                        "<li>Items that are $20 or more will be shipped with "
                        "Insurance</li></ul>")

        if EBAY_EMP:
            description += ("<h1>Notes:</h1>"
                            "<p>I am an eBay employee, and follow the eBay "
                            "employee trading and community content policy. "
                            "For more info, see <a href='http://pages.ebay.com"
                            "/help/policies/everyone-employee.html'>Employee "
                            "Policies</a></p>")

        # Add styles
        description = description.replace("<p>", "<p style='font: 100%/1.5 "
                                          "Arial, sans-serif; font-size: 1em; "
                                          " line-height: 1.5; margin: 0 0 "
                                          "1em;'>")
        description = description.replace("<li>", "<li style='font: 100%/1.5 "
                                          "Arial, sans-serif; font-size: 1em; "
                                          " line-height: 1.5; margin: 0 0 "
                                          "1em;'>")
        description = description.replace("<h1>", "<h1 style='font: 100%/1.5 "
                                          "Arial, sans-serif; font-size: "
                                          "2em;'>")
        description = cgi.escape(description)

        condition_desc = ""

        if card.condition == "M":
            condition_desc = re.sub('<[^<]+?>', '', nm_desc)
        elif card.condition == "EX":
            condition_desc = re.sub('<[^<]+?>', '', ex_desc)
        elif card.condition == "VG":
            condition_desc = re.sub('<[^<]+?>', '', vg_desc)
        elif card.condition == "G":
            condition_desc = re.sub('<[^<]+?>', '', g_desc)

        shipping = {
            "ExcludeShipToLocation": ['Middle East', 'BB', 'BZ', 'PF',
                                      'MX', 'RU', 'AT', 'HR', 'CZ',
                                      'EE', 'GI', 'IT', 'LV', 'RO',
                                      'ZA', 'BR', 'UY', 'VN', 'AF', 'LK'],
            "ShippingType": "Flat",
            "ShippingServiceOptions": {
                "ShippingServicePriority": "1",
                "ShippingService": "USPSFirstClass",
                "ShippingServiceCost": "0.00"
            },
            "InternationalShippingServiceOption": {
                "ShipToLocation": "WorldWide",
                "ShippingServicePriority": "1",
                "ShippingService": "USPSFirstClassMailInternational",
                "ShippingServiceCost": str(INTL_SHIPPING)
            },
            "GlobalShipping": "false",
        }

        myitem = {
            "Item": {
                "Title": title,
                "Description": description,
                "ConditionDescription": condition_desc,
                "PrimaryCategory": {"CategoryID": self.category_id},
                "Country": "US",
                "ConditionID": "3000",
                "Currency": "USD",
                "Quantity": card.quantity,
                "ListingDuration": "GTC",
                "StartPrice": card.ebay_price,
                "Location": LOCATION,
                "PaymentMethods": "PayPal",
                "PayPalEmailAddress": PAYPAL_ADDRESS,
                "PictureDetails": {"PictureURL": self.photo_url},
                "Storefront": {"StoreCategoryID": STORE_CATEGORY_ID},

                "ReturnPolicy": {
                    "ReturnsAcceptedOption": "ReturnsAccepted",
                    "RefundOption": "MoneyBack",
                    "ReturnsWithinOption": "Days_14",
                    "Description": "If you are not satisfied, return the item "
                                   "for refund.",
                    "ShippingCostPaidByOption": "Buyer"
                },
                "ShippingPackageDetails": {
                    "PackageDepth": 1,
                    "PackageLength": 6,
                    "PackageWidth": 9,
                    "WeightMajor": 0,
                    "WeightMinor": 1,
                },

                "ShippingDetails": shipping,
                "DispatchTimeMax": 1,
                "ItemSpecifics": {
                    "NameValueList": [
                        {
                            "Name": "Brand",
                            "Value": "Wizards of the Coast"
                        },
                        {
                            "Name": "Character Family",
                            "Value": "Magic the Gathering"
                        },
                        {
                            "Name": "Card Rarity",
                            "Value": card.get_rarity_display()
                        },
                        {
                            "Name": "Language",
                            "Value": "English"
                        },
                        {
                            "Name": "Edition",
                            "Value": card.edition
                        }
                    ]
                }
            }
        }

        return myitem

    def ListCard(self, card):
        logger.info("Uploading photo for %s" % card)
        self.UploadPhoto(card.multiverse_id, card.name)

        item = self.GetListingData(card)
        try:
            logger.info("Creating eBay listing for %s with quantity %d" %
                        (card, item['Item']['Quantity']))
            response = self.api.execute('AddFixedPriceItem', item)
            data = json.loads(response.json())
            item_id = data['ItemID']
            return item_id

        except ConnectionError as e:
            logger.error(str(e))

    def UpdateCard(self, card):
        response = self.api.execute('GetItem', {'ItemID': card.ebay_item_id})
        data = json.loads(response.json())
        quantity = int(data['Item']['Quantity'])
        quantity_sold = int(data['Item']['SellingStatus']['QuantitySold'])
        self.photo_url = data['Item']['PictureDetails']['PictureURL']

        item = self.GetListingData(card)
        item['Item']['ItemID'] = card.ebay_item_id

        net_quantity = quantity - quantity_sold

        logger.debug("%s - quantity = %d/%d/%d, price = %.2f/%.2f" % (
                     card, card.quantity, quantity, quantity_sold,
                     float(card.ebay_price),
                     float(data['Item']['StartPrice']['value'])))

        if card.quantity > net_quantity:
            logger.info("Setting local quantity for %s from %d to %d" % (
                        card, card.quantity, net_quantity))
            card.quantity = net_quantity
            card.save()

        if card.quantity == 0:
            logger.info("Deleting %s as there are 0 quantity available" % card)
            card.delete()
            return

        if ((card.quantity == net_quantity and
             float(card.ebay_price) ==
             float(data['Item']['StartPrice']['value']))):
            return

        if card.ebay_price > MAX_AUTO_LIST:
            logger.warning("Price for %s is over threshold for auto-listing - "
                           "skipping" % card.name)
            return

        try:
            logger.info("Updating eBay listing for %s - quantity = %d, "
                        "price = %.2f" % (card, item['Item']['Quantity'],
                                          card.ebay_price))
            response = self.api.execute('ReviseFixedPriceItem', item)

        except ConnectionError as e:
            logger.error(str(e))
