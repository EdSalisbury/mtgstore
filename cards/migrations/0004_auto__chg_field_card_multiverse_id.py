# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Card.multiverse_id'
        db.alter_column(u'cards_card', 'multiverse_id', self.gf('django.db.models.fields.PositiveIntegerField')())

    def backwards(self, orm):

        # Changing field 'Card.multiverse_id'
        db.alter_column(u'cards_card', 'multiverse_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

    models = {
        u'cards.card': {
            'Meta': {'object_name': 'Card'},
            'condition': ('django.db.models.fields.CharField', [], {'default': "'M'", 'max_length': '2'}),
            'edition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cards.Edition']"}),
            'foil': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'multiverse_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
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