# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-18 06:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web', '0006_auto_20161014_0209'),
    ]

    operations = [
        migrations.CreateModel(
            name='cmd_log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=32)),
                ('cmd', models.CharField(max_length=64)),
                ('exec_time', models.DateTimeField(auto_now_add=True)),
                ('name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u65e5\u5fd7\u8868',
                'verbose_name_plural': '\u65e5\u5fd7\u8868',
            },
        ),
    ]
