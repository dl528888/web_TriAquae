# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'HostLog.result'
        db.add_column(u'triWeb_hostlog', 'result',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=30),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'HostLog.result'
        db.delete_column(u'triWeb_hostlog', 'result')


    models = {
        u'triWeb.connectionmethod': {
            'Meta': {'object_name': 'ConnectionMethod'},
            'addtional_info': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'protocol': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'triWeb.dailyweather': {
            'Meta': {'object_name': 'DailyWeather'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'day': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month': ('django.db.models.fields.IntegerField', [], {}),
            'rainfall': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '1'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'temperature': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        },
        u'triWeb.group': {
            'Meta': {'object_name': 'Group'},
            'group_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_group': ('django.db.models.fields.CharField', [], {'default': "'TOPGROUP'", 'max_length': '30'})
        },
        u'triWeb.hostlog': {
            'Meta': {'object_name': 'HostLog'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event_log': ('django.db.models.fields.TextField', [], {}),
            'event_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'triWeb.ip': {
            'Meta': {'object_name': 'IP'},
            'agent': ('django.db.models.fields.CharField', [], {'default': "'NO'", 'max_length': '20'}),
            'creater': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['triWeb.User']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'group_name': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'GroupZone'", 'symmetrical': 'False', 'to': u"orm['triWeb.Group']"}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'primary_key': 'True'}),
            'monitor_status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['triWeb.MonitorMethod']"}),
            'online_date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'opreating_system': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'ping_status': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'port': ('django.db.models.fields.IntegerField', [], {'default': '22', 'max_length': '7'}),
            'protocol_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['triWeb.ConnectionMethod']", 'null': 'True'}),
            'server_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'triWeb.monitormethod': {
            'Meta': {'object_name': 'MonitorMethod'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monitor_method': ('django.db.models.fields.CharField', [], {'default': "'ping'", 'max_length': '20'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'triWeb.monthlyweatherbycity': {
            'Bejing_temp': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '1'}),
            'Meta': {'object_name': 'MonthlyWeatherByCity'},
            'ShangHai_temp': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month': ('django.db.models.fields.IntegerField', [], {})
        },
        u'triWeb.pingstatusvalue': {
            'Meta': {'object_name': 'PingStatusValue'},
            'check_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['triWeb.IP']"}),
            'ping_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2'})
        },
        u'triWeb.user': {
            'Meta': {'object_name': 'User'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'group_name': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['triWeb.Group']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.IntegerField', [], {'max_length': '13'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['triWeb']