# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Edition'
        db.create_table(u'cards_edition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('set_id', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'cards', ['Edition'])

        # Adding model 'Card'
        db.create_table(u'cards_card', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('edition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cards.Edition'])),
            ('foil', self.gf('django.db.models.fields.BooleanField')()),
            ('condition', self.gf('django.db.models.fields.CharField')(default='M', max_length=2)),
            ('quantity', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
        ))
        db.send_create_signal(u'cards', ['Card'])


    def backwards(self, orm):
        # Deleting model 'Edition'
        db.delete_table(u'cards_edition')

        # Deleting model 'Card'
        db.delete_table(u'cards_card')


    models = {
        u'cards.card': {
            'Meta': {'object_name': 'Card'},
            'condition': ('django.db.models.fields.CharField', [], {'default': "'M'", 'max_length': '2'}),
            'edition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cards.Edition']"}),
            'foil': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        u'cards.edition': {
            'Meta': {'object_name': 'Edition'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'set_id': ('django.db.models.fields.CharField', [], {'max_length': '6'})
        }
    }

    complete_apps = ['cards']