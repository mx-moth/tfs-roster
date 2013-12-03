# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Shift'
        db.create_table(u'schedules_shift', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('station', self.gf('django.db.models.fields.related.ForeignKey')(related_name='shifts', to=orm['people.Station'])),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('start', self.gf('django.db.models.fields.TimeField')()),
            ('end', self.gf('django.db.models.fields.TimeField')()),
        ))
        db.send_create_signal(u'schedules', ['Shift'])

        # Adding model 'Availability'
        db.create_table(u'schedules_availability', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='schedule', to=orm['people.Person'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('start', self.gf('django.db.models.fields.TimeField')()),
            ('end', self.gf('django.db.models.fields.TimeField')()),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('truck', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Truck'], null=True, blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'schedules', ['Availability'])


    def backwards(self, orm):
        # Deleting model 'Shift'
        db.delete_table(u'schedules_shift')

        # Deleting model 'Availability'
        db.delete_table(u'schedules_availability')


    models = {
        u'people.person': {
            'Meta': {'ordering': "('rank__order', 'name')", 'object_name': 'Person'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'qualifications': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['people.Qualification']", 'symmetrical': 'False', 'blank': 'True'}),
            'rank': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['people.Rank']"}),
            'station': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'people'", 'to': u"orm['people.Station']"})
        },
        u'people.qualification': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Qualification'},
            'class_name': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'people.rank': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Rank'},
            'class_name': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '-1'})
        },
        u'people.station': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Station'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'people.truck': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Truck'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'station': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['people.Station']"})
        },
        u'schedules.availability': {
            'Meta': {'ordering': "('date', 'start', 'status')", 'object_name': 'Availability'},
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'end': ('django.db.models.fields.TimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'schedule'", 'to': u"orm['people.Person']"}),
            'start': ('django.db.models.fields.TimeField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'truck': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['people.Truck']", 'null': 'True', 'blank': 'True'})
        },
        u'schedules.shift': {
            'Meta': {'ordering': "('station', 'start')", 'object_name': 'Shift'},
            'end': ('django.db.models.fields.TimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'start': ('django.db.models.fields.TimeField', [], {}),
            'station': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shifts'", 'to': u"orm['people.Station']"})
        }
    }

    complete_apps = ['schedules']