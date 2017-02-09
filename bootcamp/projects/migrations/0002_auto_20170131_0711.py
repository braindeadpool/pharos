# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-31 07:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0002_auto_20170131_0711'),
        ('samples', '0002_auto_20170131_0711'),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='devices',
            field=models.ManyToManyField(blank=True, null=True, to='devices.Device'),
        ),
        migrations.AddField(
            model_name='project',
            name='samples',
            field=models.ManyToManyField(blank=True, null=True, to='samples.Sample'),
        ),
    ]