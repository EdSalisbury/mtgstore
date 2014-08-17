# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Card.price_low'
        db.add_column(u'cards_card', 'price_low',
                      self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=10, decimal_places=2),
                      keep_default=False)

        # Adding field 'Card.price_med'
        db.add_column(u'cards_card', 'price_med',
                      self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=10, decimal_places=2),
                      keep_default=False)

        # Adding field 'Card.price_high'
        db.add_column(u'cards_card', 'price_high',
                      self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=10, decimal_places=2),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Card.price_low'
        db.delete_column(u'cards_card', 'price_low')

        # Deleting field 'Card.price_med'
        db.delete_column(u'cards_card', 'price_med')

        # Deleting field 'Card.price_high'
        db.delete_column(u'cards_card', 'price_high')


    models = {
        u'cards.card': {
            'Meta': {'object_name': 'Card'},
            'condition': ('django.db.models.fields.CharField', [], {'default': "'M'", 'max_length': '2'}),
            'edition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cards.Edition']"}),
            'foil': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'multiverse_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'price_high': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '10', 'decimal_places': '2'}),
            'price_low': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '10', 'decimal_places': '2'}),
            'price_med': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '10', 'decimal_places': '2'}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        u'cards.edition': {
            'Meta': {'object_name': 'Edition'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'set_id': ('django.db.models.fields.CharField', [], {'max_length': '6'})
        }
    }

    complete_apps = ['cards']