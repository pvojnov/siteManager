# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-28 09:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servers', '0002_auto_20161227_1846'),
    ]

    operations = [
        migrations.RenameField(
            model_name='server',
            old_name='envirnment',
            new_name='environment',
        ),
        migrations.RenameField(
            model_name='service',
            old_name='envirnment',
            new_name='environment',
        ),
        migrations.AddField(
            model_name='server',
            name='action',
            field=models.CharField(choices=[(b'START', b'Start'), (b'STOP', b'Stop'), (b'RESTART', b'Restart'), (b'RELOAD', b'Reload'), (b'NONE', b'None')], default=b'NONE', max_length=25),
        ),
        migrations.AddField(
            model_name='service',
            name='action',
            field=models.CharField(choices=[(b'START', b'Start'), (b'STOP', b'Stop'), (b'RESTART', b'Restart'), (b'RELOAD', b'Reload'), (b'NONE', b'None')], default=b'NONE', max_length=25),
        ),
        migrations.AlterField(
            model_name='server',
            name='status',
            field=models.CharField(choices=[(b'STARTED', b'Started'), (b'STOPED', b'Stoped'), (b'RESTARTING', b'Restarting'), (b'RELOADING', b'Reloading'), (b'PENDING', b'Pending')], default=b'PENDING', max_length=25),
        ),
        migrations.AlterField(
            model_name='service',
            name='status',
            field=models.CharField(choices=[(b'STARTED', b'Started'), (b'STOPED', b'Stoped'), (b'RESTARTING', b'Restarting'), (b'RELOADING', b'Reloading'), (b'PENDING', b'Pending')], default=b'PENDING', max_length=25),
        ),
    ]
