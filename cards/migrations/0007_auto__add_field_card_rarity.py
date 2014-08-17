# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Card.rarity'
        db.add_column(u'cards_card', 'rarity',
                      self.gf('django.db.models.fields.CharField')(default='C', max_length=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Card.rarity'
        db.delete_column(u'cards_card', 'rarity')


    models = {
        u'cards.card': {
            'Meta': {'object_name': 'Card'},
            'condition': ('django.db.models.fields.CharField', [], {'default': "'M'", 'max_length': '2'}),
            'ebay_item_id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'ebay_price': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '10', 'decimal_places': '2'}),
            'edition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cards.Edition']"}),
            'foil': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'multiverse_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'price_high': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '10', 'decimal_places': '2'}),
            'price_low': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '10', 'decimal_places': '2'}),
            'price_med': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '10', 'decimal_places': '2'}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'rarity': ('django.db.models.fields.CharField', [], {'default': "'C'", 'max_length': '1'})
        },
        u'cards.edition': {
            'Meta': {'object_name': 'Edition'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'set_id': ('django.db.models.fields.CharField', [], {'max_length': '6'})
        }
    }

    complete_apps = ['cards']