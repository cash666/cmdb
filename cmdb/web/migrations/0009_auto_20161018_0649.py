# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-18 06:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_cmd_log_hostname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cmd_log',
            name='name',
            field=models.CharField(default='', max_length=32),
        ),
    ]
