"""Django Admin module"""

from django.contrib import admin
from cards.models import Edition, Card


class EditionAdmin(admin.ModelAdmin):
    """Displays Editions in a nice list."""
    list_display = ('set_id', 'name')


class CardAdmin(admin.ModelAdmin):
    """Displays cards in a nice list."""
    list_display = ('name', 'foil', 'edition', 'rarity', 'condition',
                    'quantity', 'price_low', 'price_med', 'price_high',
                    'ebay_price', 'ebay_item_id')

admin.site.register(Edition, EditionAdmin)
admin.site.register(Card, CardAdmin)
