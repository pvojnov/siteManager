# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-05 11:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('servers', '0005_auto_20161229_1159'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnsibleLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cmd', models.CharField(max_length=1000)),
                ('respone', models.TextField(blank=True, null=True)),
                ('error', models.TextField(blank=True, null=True)),
                ('success', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='servers.Service')),
            ],
        ),
    ]