# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'IP.monitor_status'
        db.add_column('triWeb_ip', 'monitor_status',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['triWeb.MonitorMethod']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'IP.monitor_status'
        db.delete_column('triWeb_ip', 'monitor_status_id')


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