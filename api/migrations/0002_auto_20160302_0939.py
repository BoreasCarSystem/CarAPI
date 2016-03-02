# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-02 09:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='id',
        ),
        migrations.AlterField(
            model_name='message',
            name='type',
            field=models.CharField(choices=[('AC_enabled', 'Set air condition status'), ('AC_temperature', 'Set air condition temperature')], max_length=30, primary_key=True, serialize=False),
        ),
    ]
