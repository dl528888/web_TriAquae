# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Group'
        db.create_table('triWeb_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('parent_group', self.gf('django.db.models.fields.CharField')(default='TOPGROUP', max_length=30)),
        ))
        db.send_create_signal('triWeb', ['Group'])

        # Adding model 'User'
        db.create_table('triWeb_user', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('phone', self.gf('django.db.models.fields.IntegerField')(max_length=13)),
        ))
        db.send_create_signal('triWeb', ['User'])

        # Adding M2M table for field group_name on 'User'
        db.create_table('triWeb_user_group_name', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm['triWeb.user'], null=False)),
            ('group', models.ForeignKey(orm['triWeb.group'], null=False))
        ))
        db.create_unique('triWeb_user_group_name', ['user_id', 'group_id'])

        # Adding model 'MonitorMethod'
        db.create_table('triWeb_monitormethod', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('monitor_method', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('triWeb', ['MonitorMethod'])

        # Adding model 'IP'
        db.create_table('triWeb_ip', (
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15, primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('server_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('port', self.gf('django.db.models.fields.IntegerField')(default=22, max_length=7)),
            ('opreating_system', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('agent', self.gf('django.db.models.fields.CharField')(default='NO', max_length=20)),
            ('online_date', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('creater', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['triWeb.User'])),
            ('monitor_status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['triWeb.MonitorMethod'])),
        ))
        db.send_create_signal('triWeb', ['IP'])

        # Adding M2M table for field group_name on 'IP'
        db.create_table('triWeb_ip_group_name', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ip', models.ForeignKey(orm['triWeb.ip'], null=False)),
            ('group', models.ForeignKey(orm['triWeb.group'], null=False))
        ))
        db.create_unique('triWeb_ip_group_name', ['ip_id', 'group_id'])


    def backwards(self, orm):
        # Deleting model 'Group'
        db.delete_table('triWeb_group')

        # Deleting model 'User'
        db.delete_table('triWeb_user')

        # Removing M2M table for field group_name on 'User'
        db.delete_table('triWeb_user_group_name')

        # Deleting model 'MonitorMethod'
        db.delete_table('triWeb_monitormethod')

        # Deleting model 'IP'
        db.delete_table('triWeb_ip')

        # Removing M2M table for field group_name on 'IP'
        db.delete_table('triWeb_ip_group_name')


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
            'monitor_method': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
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