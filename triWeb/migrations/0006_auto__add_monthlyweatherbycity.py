# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MonthlyWeatherByCity'
        db.create_table('triWeb_monthlyweatherbycity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('month', self.gf('django.db.models.fields.IntegerField')()),
            ('Bejing_temp', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=1)),
            ('ShangHai_temp', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=1)),
        ))
        db.send_create_signal('triWeb', ['MonthlyWeatherByCity'])


    def backwards(self, orm):
        # Deleting model 'MonthlyWeatherByCity'
        db.delete_table('triWeb_monthlyweatherbycity')


    models = {
        'triWeb.group': {
            'Meta': {'object_name': 'Group'},
            'group_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_group': ('django.db.models.fields.CharField', [], {'default': "'TOPGROUP'", 'max_length': '30'})
        },
        'triWeb.ip': {
            'Meta': {'object_name': 'IP'},
            'agent': ('django.db.models.fields.CharField', [], {'default': "'NO'", 'max_length': '20'}),
            'creater': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['triWeb.User']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'group_name': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'GroupZone'", 'symmetrical': 'False', 'to': "orm['triWeb.Group']"}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'primary_key': 'True'}),
            'monitor_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['triWeb.MonitorMethod']"}),
            'online_date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'opreating_system': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'ping_status': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'port': ('django.db.models.fields.IntegerField', [], {'default': '22', 'max_length': '7'}),
            'server_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'triWeb.monitormethod': {
            'Meta': {'object_name': 'MonitorMethod'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monitor_method': ('django.db.models.fields.CharField', [], {'default': "'ping'", 'max_length': '20'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'triWeb.monthlyweatherbycity': {
            'Bejing_temp': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '1'}),
            'Meta': {'object_name': 'MonthlyWeatherByCity'},
            'ShangHai_temp': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month': ('django.db.models.fields.IntegerField', [], {})
        },
        'triWeb.user': {
            'Meta': {'object_name': 'User'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'group_name': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['triWeb.Group']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.IntegerField', [], {'max_length': '13'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['triWeb']