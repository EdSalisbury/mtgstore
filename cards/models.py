from django.db import models


class Edition(models.Model):
    set_id = models.CharField(max_length=6)
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


class Card(models.Model):
    COND_M = 'M'
    COND_EX = 'EX'
    COND_VG = 'VG'
    COND_G = 'G'

    COND_CHOICES = (
        (COND_M, "NM/M"),
        (COND_EX, "EX"),
        (COND_VG, "VG"),
        (COND_G, "G"))

    RARITY_M = 'M'
    RARITY_R = 'R'
    RARITY_U = 'U'
    RARITY_C = 'C'

    RARITY_CHOICES = (
        (RARITY_M, "Mythic Rare"),
        (RARITY_R, "Rare"),
        (RARITY_U, "Uncommon"),
        (RARITY_C, "Common"))

    name = models.CharField(max_length=64)
    edition = models.ForeignKey(Edition)
    foil = models.BooleanField()
    rarity = models.CharField(max_length=1, choices=RARITY_CHOICES,
                              default=RARITY_C)
    condition = models.CharField(max_length=2, choices=COND_CHOICES,
                                 default=COND_M)
    multiverse_id = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)
    price_low = models.DecimalField(max_digits=10, decimal_places=2,
                                    default=0.0)
    price_med = models.DecimalField(max_digits=10, decimal_places=2,
                                    default=0.0)
    price_high = models.DecimalField(max_digits=10, decimal_places=2,
                                     default=0.0)
    ebay_price = models.DecimalField(max_digits=10, decimal_places=2,
                                     default=0.0)
    ebay_item_id = models.CharField(max_length=32, blank=True)

    def __unicode__(self):
        if self.foil:
            return "%s FOIL (%s) - %s" % (self.name, self.edition,
                                          self.condition)

        return "%s (%s) - %s" % (self.name, self.edition, self.condition)
